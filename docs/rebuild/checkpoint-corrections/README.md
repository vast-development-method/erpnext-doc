# September operation catalog corrections

The September inventory declares 33,360 distinct operations. The archived index contains 33,371 rows but resolves only 33,318 distinct bodies. Fifty-three identical enterprise definitions occur twice, and 42 stock-controller definitions have declarations but no body or index row. Counting the index rows therefore overstates the coverage.

The [recovered stock-controller contracts](stock-controller.json) supply the 42 missing decisions. Each names the original inventory identifier and call parameters, links to the exact September ERPNext source lines, describes the decisions in execution order, and gives a worked acceptance example. Fifteen operations dispatch to services and include the receiving implementation in their source references. The [duplicate register](duplicates.json) gives both locations and the common body digest for each repeated identifier. These corrections apply to [the September source revisions](../model/pins.json).

| Domain | Declared identifiers | Archived body rows | Unique archived bodies | Corrected identifiers available |
|---|---:|---:|---:|---:|
| Enterprise | 16,038 | 16,049 | 15,996 | 16,038 |
| Foundation | 13,005 | 13,005 | 13,005 | 13,005 |
| Workforce | 2,780 | 2,780 | 2,780 | 2,780 |
| Relationships | 1,537 | 1,537 | 1,537 | 1,537 |
| **Total** | **33,360** | **33,371** | **33,318** | **33,360** |

## Look up a contract

From a source checkout, assemble the edition using the [reading guide](../../../checkpoints/reading-guide.md). The following commands use the example destination supplied in that guide. The optional Python 3.8+ reader uses only the standard library. An implementation in any language can apply the same join.

```sh
python3 docs/rebuild/checkpoint-corrections/resolve.py ../erpnext-blueprint-expanded
python3 docs/rebuild/checkpoint-corrections/resolve.py ../erpnext-blueprint-expanded operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_get_delivery_note_billing_percentage
```

For a lookup the result includes the inventory declaration, the resolved body, its origin and the path within the indicated edition. The same reader can run from inside an assembled directory with `.` as its edition argument. A complete scan requires reading the decision partitions for the four applications. Omit the identifier to obtain the coverage counts; an unknown identifier or unsuccessful check exits with an error.

1. Read the operation inventories in manifest order, keyed by their unique identifiers. Join against actual bodies in the four decision-contract manifests.
2. For an archived body, look up the identifier in the partition. For a duplicated identifier, the lexicographically first listed partition is canonical. Both complete decoded bodies must match the registered digest. The reader also reconciles every index row to its actual partition, including multiplicity.
3. For a declaration with no archived body, match its identifier to the correction catalog. Confirm the name, scope, owner and parameter bindings against the declaration. Reject an absent or unexpected correction, undeclared body, conflicting duplicate, or incorrect pointer.
4. Interpret an archived decision using its decision-semantics catalog. Interpret a recovered one using its ordered business steps and worked example. The coverage count measures resolvable contracts. Runtime equivalence for these operations requires exercising the published scenarios against the chosen reference and replacement.

## Three business decisions restored by the join

| Action | Reference decision |
|---|---|
| Bill a delivery after a rate change | Ten units delivered at 10 and all ten invoiced for 80 can still reach 100% billed. The delivery’s own calculation compares the capped amount basis and its quantity-based allocation for each line. |
| Apply a subcontracting reservation | For an untracked material, five units can consume 3 units of the first eligible reservation and 2 of the next. The operation updates each reservation, its linked voucher and the stock bin. |
| Request a ledger preview | The preview checks the operator’s read access to the voucher, builds the accounting or stock view, rolls back the preview transaction and returns the columns and rows. |

The 42 contracts describe the September development revision. A release-specific workflow can differ after a refactor or accounting change. The [November trading evidence](../live/README.md) records the reference release and observed ledger examples for that edition.
