# Compare a replacement with the reference site

Use these two small observation files as expected outputs when a replacement can run the [integrated trading scenario](../integrated/README.md). Each preserves 12 voucher-level account and stock effects, six customer-open-item snapshots and 15 closing controls observed on the reference site. They differ in one input preparation step before submission of the partial credit note. Both produced exactly the same general-ledger and stock movements. Their open invoices differ by **69.00**.

| Expected observation | Applicable preparation |
|---|---|
| [Recalculated partial credit](recalculated.json) | Change the mapped credit quantity, then recalculate its draft taxes and totals. On submission its 69.00 reduces the original sales invoice. |
| [Stale mapped partial credit](stale-mapped.json) | Change the quantity while retaining the full mapped draft total before submit. The controller's allocation decision leaves the credit as its own open item. |

The [site evidence](../live/README.md) identifies the versions, experimental setup and original reports. The compact files here were mechanically projected from the live capture. A replacement built around semantic business commands can declare which input-preparation path it supports. A transport that claims compatibility with the upstream full-document save path also needs a decision about stale supplied totals.

## Adapter contract

The [observation schema](observation.schema.json) defines the portable JSON exchange format. Submit the commands in the [fixture](../integrated/cost-flow.json) to the candidate. Read back submitted records, stock movements, general ledger and party allocations from the candidate itself. Preserve separately identified expected and observed data.

- Map generated voucher identifiers to their corresponding fixture events, such as the first receipt to GR1. Resolve both sides of every payment allocation. CREDIT→SALE and CREDIT→CREDIT are economically different.
- Under each event, sum debit less credit by account and aggregate the signed quantity and carrying-value change per item. Compare the two warehouses independently through their assigned accounts. Quantities include their signs, and money uses base currency. Emit decimal strings.
- After each customer checkpoint, record the original invoice balance, the total customer balance and the payment ledger edges. Once the credit exists, report its own remaining balance and its original sale reference. The closing `customer_outstanding` field in this comparison means the outstanding amount on the **original invoice**. The `party_total` at the final checkpoint is the customer's net position.
- Preserve checkpoint and event order. A single source-to-target allocation can be physically split across several rows. The comparator aggregates rows sharing that exact pair and preserves pairs with different targets. It reports missing events, changed decisions and balance differences by JSON path.

Run the [comparator](compare.py) with an observation from a candidate implementation. A report from the included reference-site runner can be consumed directly. A portable file also works as input, so any programming language can produce the candidate side.

```sh
python3 docs/rebuild/comparison/compare.py compare \
  docs/rebuild/comparison/recalculated.json candidate-observations.json
```

Exit status 0 means the observable effects selected by this comparison agree, 1 reports economic differences, and 2 reports unreadable or malformed input. To demonstrate the sensitivity of the check using only committed files, compare the two observed reference paths.

```sh
python3 docs/rebuild/comparison/compare.py compare \
  docs/rebuild/comparison/recalculated.json docs/rebuild/comparison/stale-mapped.json
```

The second command intentionally returns 1. Its output identifies the credit's allocation target, original and credit invoice balances and closing outstanding amount. The observation view excludes local voucher names, framework identifiers, the transport shape, authentication, precision behaviour beyond this fixture, recovery timing and provider interactions. Separate contracts cover those concerns.
