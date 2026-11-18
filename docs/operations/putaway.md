# Allocating incoming stock

A putaway rule sets the capacity for one item at one warehouse in the owning company. An active rule requires an enabled leaf warehouse, a stock item and a priority of at least one. Duplicate item/warehouse rules fail. Rule capacity in stock units equals configured capacity multiplied by its unit conversion factor. The rule validator compares that result with the current stock balance. A capacity exactly equal to that balance leaves zero space available. The capacity read operation checks access to the rule. The allocation operation accepts purchase receipt and stock entry rows, checks write permission for the requested document type, company restrictions, item read access and access to referenced tracking bundles.

## Allocation contract

1. Resolve the incoming row's unit factor. Use the supplied nonzero factor or look up the item's unit conversion, falling back to one when unavailable. Multiply accepted transaction quantity by this factor to obtain pending stock units. Keep rejected quantity separate.
2. Load enabled company/item rules and calculate free space as the greater of zero and stock capacity less the current stock balance. Exclude the row's source warehouse. Allocate by ascending priority and then descending free space. Cache the item rules for the whole call. Splits or repeated source rows consume the same in-memory destination capacity.
3. Take the smaller of pending stock units and free space. Divide by the row factor, and for a whole transaction unit take the floor. Recalculate allocated stock units from that whole quantity. If a higher-priority warehouse fits less than one whole unit, continue to the next warehouse.
4. Write destination and quantity on each split. Purchase receipt rows store accepted stock quantity and received quantity including that split's rejected units. Stock entry rows store transferred stock quantity. A rejected quantity and its rejected tracking bundle stay on the first split. Decrease both the pending requirement and the candidate's free space.
5. Distinguish absence of a rule from insufficient room under existing rules. With no eligible rule the row retains its fallback warehouse. With insufficient capacity the operator sees the unassigned quantity. If a changed, nonempty replacement table was built, the receipt contains only those accommodated rows plus other retained rows. If no replacement rows were produced, the routine leaves the input table intact. Re-read the returned table and reconcile any warning to the original demand.

## Tracking and repeat saves

For serial text, consume identities in input order by the allocated **stock quantity**. For selected tracking bundles, partition original entries in order and allow one batch entry to span destinations. Each inward split carries its destination warehouse. When a split requires copies, a client preview copies the original bundle for each share, while a saved operation can retain its identifier on the first share. A single unchanged outward bundle can retain its identity when only the destination changes. A repeat save with equivalent allocation avoids rebuilding rows. Preserve source links on all splits so subsequent valuation and returns can identify the actual lot.

| Acceptance case | Expected observation |
|---|---|
| Receive two whole 1,000 kg bags. Priority 1 fits 500 kg and priority 2 fits 2,000 kg. | One row for two bags at priority 2, carrying 2,000 stock units. |
| Two transfer rows from different warehouses each offer ten units to the same initially empty ten-unit destination. | Exactly ten units are allocated to that destination across both source rows. |
| Source contains ten units each of batches B1 and B2. Pick five from B2 into warehouses with room for three and two. | B1 stays at ten in source. B2 balances become five in source, three and two in destinations. A repeated save preserves the rows. |
| Receive five accepted and two rejected units. Split accepted stock three and two. | First split contains three accepted, two rejected and the rejected bundle. Second has two accepted and zero rejected. |

 The capacity shared by input rows is scoped to one allocation call. A simultaneous receipt on a different connection requires its own contention test.
