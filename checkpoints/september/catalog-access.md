# Reading the September catalogs

The September checkpoint contains 100 Markdown pages, 3,375 JSON files and the license. This reader publishes all 100 pages, all 65 top-level JSON contracts and manifests, all 166 additional record definitions linked by the business chapters and four example decision partitions. The 235 published JSON files reproduce the archive bytes. The [member inventory](members.tsv) identifies the original path, byte length, SHA-256 and reading location for each of the 3,476 members.

## Follow a business question

| Question | Start here | Inspect a machine-readable result |
|---|---|---|
| How does the system value an incoming item? | [Inventory and valuation](docs/domains/inventory-and-valuation.md) | Search for `operation_enterprise_stock_utils_business_behavior_get_incoming_rate` in the [stock valuation decisions](schemas/operations/enterprise-decision-contracts/part-0947.json). The [inventory cases](schemas/mathematics/inventory-acceptance-cases.json) give expected financial and quantity effects. |
| How do attendance and leave affect a salary slip? | [Attendance and leave](docs/domains/attendance-and-leave.md) · [Payroll and benefits](docs/domains/payroll-and-benefits.md) | Find `salary_slip_get_payment_days` in the [payroll decisions](schemas/operations/workforce-decision-contracts/part-0124.json), then use the [workforce calculation cases](schemas/mathematics/workforce-acceptance-cases.json). |
| What happens when an operator converts a lead into a deal? | [Customer relationships and sales](docs/domains/customer-relationships-and-sales.md) | Find `lead_convert_to_deal` in the [customer relationship decisions](schemas/operations/relationships-decision-contracts/part-0036.json). |
| Which record fields can hold values? | [Persistence, identity and values](docs/data/persistence-identity-and-values.md) | Find `meta_get_fieldnames_with_value` in the [foundation decisions](schemas/operations/foundation-decision-contracts/part-0284.json), then read the [field semantics](schemas/data/record-value-semantics.json). |

## Read a single archive member

The catalog indexes preserve the order, entry counts and descriptions of the original partitions. A linked filename opens a file in this reader. An unlinked filename in code type identifies a bulk member. In each index, combine the displayed directory and filename to obtain its archive path. The [member inventory](members.tsv) can also be searched by name.

From the repository root, print a single named member using a shell with `cat` and `tar`. This example reads the first enterprise decision partition.

```sh
cat checkpoints/complete-specification.tar.gz.part-* | tar -xzO schemas/operations/enterprise-decision-contracts/part-0001.json
```

The archived index includes 53 repeated definitions and omits 42 stock-controller decisions. The [corrected operation lookup](../../docs/rebuild/checkpoint-corrections/README.md) resolves all 33,360 distinct IDs. To inspect the original partitions, [assemble the complete edition](../reading-guide.md). Its root contains all original paths, including the 3,140 bulk JSON members. For example, after assembly, search the operation index for a specific name or identifier. Each matching entry contains a `catalog` path relative to `schemas/operations/`. This command locates the incoming stock rate operation in the example above.

```sh
rg -l '"identifier": "operation_enterprise_stock_utils_business_behavior_get_incoming_rate"' \
  ../erpnext-blueprint-expanded/schemas/operations/operation-index
```

## Source fidelity

The member inventory records the digest of each **original** file. The reading edition adapts navigation in 39 Markdown pages and preserves the original bytes of the other 61. Every original page with its original links is in the checkpoint. The export preserves that historical snapshot and the current release supplements in separate locations. Scope labels and historical qualification claims belong to their dated source edition. The [November qualification register](../../docs/rebuild/qualification.json) tracks the subsequent evidence.
