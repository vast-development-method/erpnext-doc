# Posted FIFO, settlement and return evidence

An isolated ERPNext 16.60.0 site with Frappe 16.60.1 committed all 12 vouchers in the [receipt-to-cash example](../integrated/README.md). After each individual commit, the runner closed its database connection, opened a new one, read the submitted document, queried its GL and Stock Ledger Entries and reconciled every open supplier and customer invoice in the profile. From the first sales invoice forward, it also read the active Payment Ledger Entries by customer, source voucher and allocation target. The two applications' revisions and the database server version came from the running installation. The captured run used MariaDB 11.8.6, Python 3.14.10 and a local Redis 8.0.2 service. [Committed observation](observed.json) · [Field definitions](observation.schema.json) · [Scenario and expected balances](../integrated/cost-flow.json)

The company and the standard chart were created by the reference setup workflow using NAD, Namibia, a manufacturing domain and a calendar fiscal year. Fresh item masters selected FIFO and the stock unit Nos. Separate warehouses mapped raw and packed goods to separate stock asset accounts. Both parties, the bank, the tax accounts and the items were synthetic. There was one commercial return and one separately submitted physical return. Posting-date order and posting times were explicit for documents that support them. Purchase and sales invoices used an exclusive 15% tax and disabled rounded totals. The runner used the Administrator identity and called the reference document methods inside the Bench runtime. The included results establish the database effects under that profile. Role-specific access, HTTP transport, competing writers and worker recovery are separate qualifications. [Site adapter](run-cost-flow.py)

## Why the first credit left the invoice open

The first run reached a zero customer control-account balance, yet the original sales invoice still showed 69.00 outstanding. Selecting the original invoice as the return reference and unchecking **Update Outstanding for Self** had been insufficient. The invoice return mapper built a four-unit draft totalling −276.00. The caller edited the quantity to −1 and linked it to the separately returned delivery row. At that moment the draft retained the −276.00 grand total and a zero rounded total. The original invoice had only 96.00 outstanding. [Reproduced alternative](stale-credit.json) · [Source return mapper](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/sales_and_purchase_return.py#L600-L691)

The return validator compares the absolute rounded total, falling back to the grand total, with the original invoice's outstanding amount. A larger credit sets **Update Outstanding for Self**. That validation runs before the ordinary submit-time tax calculation. The later calculation produced the correct 69.00 credit but retained the newly enabled flag. The GL debits and credits therefore matched in both runs. The sales control line used the credit's own identity as the allocation target in the first run. Explicitly recalculating document taxes and totals after editing the quantities and before submission gave the validator −69.00, left the flag cleared and applied the credit directly to the original invoice. This path used no separate Payment Reconciliation transaction. [Outstanding guard](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/accounts_controller.py#L243-L283) · [Order of validation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/accounts_controller.py#L338-L359) · [Customer GL allocation target](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/sales_invoice.py#L1954-L1997)

| Committed event | Original invoice with fresh totals | Original invoice with stale totals in alternate run | Standalone credit with stale totals | Customer ledger net in either run |
|---|---:|---:|---:|---:|
| SALE | 276.00 | 276.00 | — | 276.00 |
| PAY1 | 96.00 | 96.00 | — | 96.00 |
| RET | 96.00 | 96.00 | — | 96.00 |
| CREDIT | 27.00 | 96.00 | −69.00 | 27.00 |
| PAY2 | 0.00 | 69.00 | −69.00 | 0.00 |
| REMIT | 0.00 | 69.00 | −69.00 | 0.00 |

The alternative submitted all vouchers on the test database and read the same ledger tables inside one transaction before rollback. The committed run settled the supplier's 266.80 and the original sales invoice in full. It ended with bank 940.20, raw inventory 5 units valued at 70.00, packed inventory 2 units valued at 64.80, gross profit 82.80 and total assets of 1,109.80. Each output includes a hash of the exact fixture. The closing statements derive from ledger totals and posted invoice balances. This adapter does not execute a financial report UI. [Committed closing controls](observed.json)

## Rejected requests

After one of four delivered units had already returned, the source rejected another four-unit return. It also rejected two two-unit return rows submitted together against the original line. After the correctly routed credit, allocating 28.00 to the original 27.00 outstanding invoice raised a validation error. Each failure records its native exception and message, rolls back its savepoint and verifies the GL, stock ledger and payment ledger row counts against their pre-attempt values. [Return combination checks](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/sales_and_purchase_return.py#L285-L371) · [Payment allocation checks](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_entry/payment_entry.py#L479-L592)

## Replay

For an offline comparison, run the following command at the blueprint repository root. It checks both stored records, the fixture hash, each account and stock movement, supplier and customer balances, Payment Ledger Entry origins and targets, rejected requests and all 15 closing measures. [Verifier](verify.py)

```sh
python3 docs/rebuild/live/verify.py
```

To regenerate the observations, start in a configured v16 Bench with the two source revisions above, MariaDB and Redis. These commands create a dedicated site with no company. Supply the new administrator and local database administrator credentials at the Bench prompts. Keep the blueprint checkout path absolute. Captures are written to a new temporary directory. The alternate case runs first so its transaction can roll back before the primary profile commits each voucher. A repeat of the committed profile needs another fresh site.

```sh
bench_root="$PWD"
read -r -p 'Absolute path to the blueprint checkout: ' blueprint_root
site=erp-fifo-witness.localhost
bench new-site "$site" --install-app erpnext
bench --site "$site" set-config allow_tests 1 --parse
bench --site "$site" set-config blueprint_witness 1 --parse
receipts=$(mktemp -d)
cd "$bench_root/sites" || exit 1
"$bench_root/env/bin/python" "$blueprint_root/docs/rebuild/live/run-cost-flow.py" \
  --site "$site" --sites-path "$bench_root/sites" \
  --credit-mode stale-mapped --output "$receipts/stale-credit.json"
"$bench_root/env/bin/python" "$blueprint_root/docs/rebuild/live/run-cost-flow.py" \
  --site "$site" --sites-path "$bench_root/sites" \
  --commit --output "$receipts/observed.json"
```

The two verifiers compare semantic voucher and account identities, decimal amounts and submission results. Native numbering and the posting date can vary when replayed in another fiscal year. Only the reference adapter depends on the upstream runtime. A replacement implementation can produce equivalent passages through its own document services, using the language-neutral inputs, posting effects and outstanding balances in the integrated fixture. [Operation contracts and expected effects](../integrated/README.md)
