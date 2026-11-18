# Stock integration tests on the reference system

Twenty selected inventory and manufacturing tests passed on a dedicated site with MariaDB. Each result names the test class and method, the immutable upstream test, its setup and its asserted outcome. The XML retains the suite and case results emitted by the test runner, with repository-relative file paths. [Individual observations](observed.json) · [JUnit results](junit.xml) · [Observation schema](observed.schema.json)

## What happened in the reference system

| Area | Cases | Outcomes |
|---|---:|---|
| Batch cost and serial selection | 4 | A linked purchase return restored the prior FIFO queue. A LIFO return against the first receipt left 5 at 100 and 10 at 200, worth 2,500. An ordinary issue of five from an explicitly selected batch took 1,000 from the newer LIFO cost layer. Expiry-based selection returned serials from the earlier-expiring batch. |
| Order reservations | 4 | Two orders each delivered their own share of the same batch. A different order could not drain another order’s reserved batch. A returned serial became eligible on a new reservation after a partial delivery. An order for three boxes of 12 reserved 24 from 25 available units. |
| Reposting | 4 | Deduplication left a later-created request queued. Restart rejected a completed rebuild and accepted a failed one. A zero-rate-enabled rebuild completed after the original receipt was cancelled. A backdated receipt raised moving average to 150 and revalued the two destination ledger rows exactly once each, to 750 and 450. |
| Manufacture and transfer | 4 | A submitted consumption entry valued at 1,000 gave a subsequent manufacture draft 750 of finished output and 250 of scrap. Two disassemblies recovered the original two raw-material batches. Manufacture rejected an unclassified extra output. A transfer posted −45 and +45 in the two stock ledgers, checked its applicable warehouse-account rule and then cancelled. |
| Stock closing | 4 | A pending rebuild blocked closing. Backdated receipt invalidated a generated closing and produced opening and closing report quantities of 15. Rolling forward batched stock preserved 10 units and 1,000 of value. When cancellation was injected after provisional balance generation, the worker removed its rows and left the closing cancelled. |

For a new implementation, use the domain rules alongside these cases. The linked purchase return and the ordinary LIFO issue use the same costing method with different valuation instructions. The work order splits a separately posted consumption value on a draft manufacture entry. The stock closing examples distinguish persisted record state from the report quantities used after invalidation. [Identity and valuation](../valuation/README.md) · [Production and disassembly](../production/README.md) · [Integrated stock and financial postings](../integrated/README.md)

## Reproduce the observations

The reference site contained the foundation and business applications with `allow_tests` enabled, MariaDB 11.8.6, Redis and Python 3.14.10. The native test suite created its fixture companies, warehouses, items and orders. Its base class rolls back after each method and clears its request caches. Fixture bootstrap also commits shared master records, so run this against a **disposable reference site**. The runner uses Python to invoke the reference system. The quantities, decisions and ledger results are portable to other implementations. [Fixture bootstrap and cleanup](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/tests/utils.py#L3009-L3041) · [Foundation test CLI](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/commands/testing.py#L287-L374)

Use a Bench with the revisions in the observation file and its normal built assets. The CLI-only environment used for this run needed an empty `sites/assets/assets.json` as a fallback for formatting fixture user welcome mail. The first setup attempt stopped during test discovery because its asset map was absent. The subsequent run used the unmodified reference test methods. Install `unittest-xml-reporting==4.0.0` in the Bench environment for per-case JUnit output. The following command runs from the documentation repository, with `ERPBENCH` set to the existing Bench directory and `SITE` to its disposable site name. [Asset resolver](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/utils/__init__.py#L976-L995) · [JUnit runner selection](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/commands/testing.py#L229-L246)

```sh
python3 docs/rebuild/stock-live/replay.py --bench "$ERPBENCH" --site "$SITE"
```

The replay checks both app Git revisions, selects the 20 named methods in five native module runs, and checks that each selected class and method returned a passing JUnit record. Unreported, skipped, failed, duplicate and unexpected cases cause a nonzero result. [Replay entry point](replay.py)

## What the observations establish

Document workflow cases call the reference test factories, document save/submit/cancel operations and the assertions named in the observations. The serial expiry selection calls the stock selector against actual serial and batch records. The transfer test chooses one GL assertion based on its fixture account mapping. Its JUnit record does not identify which accounting branch ran. [Warehouse transfer test](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_entry/test_stock_entry.py#L534-L597)

The repost and closing tests invoke worker methods synchronously or set up specific orderings. For example, one test counts each actual destination ledger update using a forwarding wrapper. Another sets the cancellation state immediately after creating provisional closing balances. These runs establish the persisted outcome for those orderings. Multi-process worker contention, inter-transaction reservation races, crash recovery and throughput require a separate concurrency harness. [Transfer replay instrumentation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py#L1203-L1243) · [Controlled closing cancellation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_closing_entry/test_stock_closing_entry.py#L499-L515)
