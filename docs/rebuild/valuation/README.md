# Valuation, tracked inventory and historical correction

These contracts extend the [inventory domain](../../domains/inventory-and-valuation.md), the [stock-count and closing workflow](../operations/inventory-control.md) and the [integrated FIFO example](../integrated/README.md) at the pinned [ERPNext v16.60.0 source revision](https://github.com/frappe/erpnext/tree/886ab6ae187244e7f1b852393384ab6019d56264).

| Rebuild question | Contract |
|---|---|
| Which rate is used when an issue has a supplied cost, stock runs negative or a returned receipt's layer has already sold? | [Moving average and rate-matched FIFO/LIFO](rates-and-layers.md) |
| Which physical units may be selected, which cost pool prices them, and which reservation is released on reversal? | [Serial/batch selection, valuation and reservation release](identity-and-reservation.md) |
| Which later vouchers and accounts change when a late receipt changes a transfer source? | [Repost scheduling, dependencies, failure and numerical trace](reposting.md) |

## Qualification

The [50 acceptance cases](acceptance.json) conform to the [Draft 2020-12 schema](acceptance.schema.json). The optional [reference witness](verify-witnesses.py) checks six pinned upstream files by hash and evaluates selected reference decisions with controlled balances, rates, date ordering, field precision and identity data. From this blueprint and an adjacent ERPNext v16.60.0 checkout:

```sh
python3 docs/rebuild/valuation/verify-witnesses.py ../erpnext
```

| Decision contract | Cases | What is compared |
|---|---:|---|
| Moving-average rate | 10 | Positive, negative, cleared and zero-cost balances; receipt, explicit issue and fallback branches |
| Layer state | 13 | Complete remaining FIFO/LIFO layers and extended stock value after the action |
| Bundle value | 3 | Signed weighted quantity, value and average rate |
| Batch picking | 4 | Allocation by supplied candidate order, including a short list |
| Tracked reservation fulfillment/release | 5 | Exact child-level deltas given already-locked ordered candidates, selected serials/batches and per-parent caps |
| Repost order | 2 | Effective time, creation time and stable insertion order |
| Permitted repost time window | 7 | Normal and overnight windows, boundaries, exempt weekday and disabled setting |
| Batch-specific cost | 4 | Eligible batches, available quantities, actual zero rates and the signed value change |
| Backdated multi-location replay | 2 | Original and corrected warehouse balances, transfer value and cost of goods sold |

The final two replay cases orchestrate the pinned moving-average decision through a small independent transfer ledger. They check the numbers in the worked example. Generating real stock and financial vouchers, database locking, queue persistence, permissions and interruption recovery require the full-site exercises in the reposting chapter. The verifier uses only the Python standard library to read the reference source; these are independently implementable business contracts.
