# Resolve an operation

The [current operation lookup](../../../schemas/operations/current-decisions/README.md) selects the applicable procedure by stable identifier. It covers enterprise transactions, foundation services, workforce and relationships. The [declaration index](../../../schemas/operations/operation-index.json) also retains the underlying 33,360 detailed research contracts.

From the repository root, audit the catalog or retrieve an individual binding.

```sh
python3 docs/rebuild/checkpoint-corrections/resolve.py
python3 docs/rebuild/checkpoint-corrections/resolve.py . operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_get_delivery_note_billing_percentage
```

The second command locates a retired stock-controller binding. Its preserved contract explains a calculation involving both amount and invoiced quantity. The lookup omits an applicable body for that binding. The [transaction progress chapter](../../operations/transaction-progress-and-row-closure.md) defines the actual delivery billing rule. For the active monetary progress calculation, look up `operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_update_billing_percentage`. If ten units delivered at 10 are directly invoiced at 8, the billed amount is 80 against 100 and the delivery is 80% billed. The lookup supplies the current procedure, scope and file for that binding.

## Reconciliation evidence

The original inventory contained 33,360 unique declarations. Its body index listed 33,371 rows, including 53 repeated definitions and omitting 42 stock-controller procedures. The [duplicate receipts](duplicates.json) record the identical body digests and previous locations. The [stock-controller receipts](stock-controller.json) preserve the reviewed decision steps and worked examples for the 42 recovered definitions. Each of the 33,360 declarations now has one body and one index entry in the preserved decision catalog. The applicability lookup separately establishes which procedure to use for a current binding.

| Business area | Unique original declarations and resolved bodies |
|---|---:|
| Enterprise | 16,038 |
| Foundation | 13,005 |
| Workforce | 2,780 |
| Relationships | 1,537 |
| **Total** | **33,360** |

The optional [reader](resolve.py) compares the actual declarations, decisions, binding ranges, current procedures and index targets. It can also audit an exported original research package against its correction receipts.
