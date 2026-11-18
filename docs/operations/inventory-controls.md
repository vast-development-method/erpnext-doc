# Stock policy and product master changes

A policy change can affect existing stock, open reservations and the interpretation of a previously issued serial number. Evaluate the proposed configuration against the affected companies, products and effective transactions before enabling it. Preserve the original inputs and accountable document on past movements. Operating dates below are business dates.

## Configuration changes

| Request | Admission decision and effect |
|---|---|
| Enable negative stock or enable stock reservations | Refuse to enable either feature while the other is active. An ordinary inventory posting still has to pass its product, warehouse and tracking checks. |
| Disable stock reservations | Require no open submitted reservation. Its open quantity is reserved less delivered, transferred and consumed. A positive remainder on any qualifying row blocks the change. With reservations off, switch automatic reservation off. |
| Disable serial or batch tracking for the installation | Refuse while a submitted tracking allocation exists or any product still has serial or batch tracking enabled. Hiding a control cannot make an existing tracked product anonymous. |
| Switch existing tracked stock from common costing to batch-specific costing | Where a submitted serial/batch allocation already exists, refuse to clear the policy that suppresses batch-specific valuation. Former allocations do not supply an independent cost history merely because the setting changed. |
| Change the general valuation method | If an active ledger movement exists for a product that inherits its method, refuse the change of an established default. An item with its own method is outside this particular default-method guard. Check product-specific cost and serial settings independently. |
| Set an inventory freeze | Check for pending valuation corrections through the proposed cutoff. A fixed cutoff includes its final day. A rolling limit of $n$ days freezes a posting when posting date plus $n$ days is on or before today. Either freeze can apply. Only the configured stock-freeze role bypasses that check. The accounting close and other posting controls still apply. |
| Enable automatic price insertion while sales fallback pricing is active | Warn that a price inherited from the default list can be written to the transaction list. This combination is allowed. Keep the source list and the saved price distinguishable on review. |

A stock manager can maintain stock settings. A sales user has read access to those settings through the base role. A role that may submit a sale or receipt does not thereby acquire the freeze override or permission to change the costing policy.

**Boundary examples.** A reservation of 10 with 3 delivered, 4 transferred and 2 consumed still has one outstanding and blocks disabling reservations. With a seven-day rolling freeze, a posting exactly seven days earlier is frozen. Enabling automatic reservation has no effect after the parent reservation policy has been disabled.

## Product admission and opening balances

| Product decision | Required checks or derived data |
|---|---|
| Customer-supplied component | Cannot be a purchase item and cannot have a nonzero valuation rate. Its material request category becomes customer-provided. A customer-supplied component remains distinguishable from a company-owned purchased component at the same workshop. |
| Fixed asset | Must be a nonstock product with an asset category. Existing inventory ledger history prevents conversion to a fixed asset. Submitted asset records prevent turning off fixed-asset status. |
| Retain a sample | Requires batch tracking and a configured sample-retention warehouse on at least one company. Removing retention clears the sample quantity. Automatic batch creation with expiry tracking requires a positive shelf life. |
| Opening quantity on a tracked stock product | Serialised products require a numbering series. Batched products require automatic batch creation. Missing valuation rate is distinct from an entered zero. The special customer-provided branch permits an absent valuation rate. |
| Opening balance destination | For each company default row, try its product warehouse, the company default warehouse and then that company's stores warehouse. For a resolved warehouse require a posting-level temporary opening account. Record the stock opening through a reconciliation with company, product, warehouse, quantity, rate and account. A zero-rate opening produces an operator notice. A company for which no destination resolves has no opening reconciliation from this action. |

For example, opening five nontracked units at 12 gives a reconciliation target of five units worth 60. Editing the product's label does not create another opening balance. When separate company default rows apply, audit the distinct company reconciliations. Each row uses the entered opening quantity, so the input is not divided between companies.

## Change measurement, tracking and substitution

A product has one stock unit and may have many transaction units. Refuse an incompatible stock-unit change when it would reinterpret submitted movements or outstanding document rows using another base unit. For an allowed change, rebuild the conversion list for the new base and ask the operator to redefine alternate factors. Existing transactions carry their original factor. Before clearing serial tracking on a formerly serialised product, check for both draft and submitted tracking allocations. Either prevents removal. Cancelled allocations alone do not trigger that guard.

A substitute relation has an original product, alternate product and direction. Reject self-substitution, duplicate ordered pairs, a mismatch in stock/nonstock status, and an original that disallows alternatives. A bidirectional relation requires both products to allow alternatives. Differences in manufacturing inclusion and serial/batch flags produce warnings, subject to the separate hard checks. A one-way relation A→B allows B to fulfil eligible demand for A. It authorises no reverse, transitive or automatic substitution. Stock, cost and traceability follow the product actually issued and the production row declaring the substitution.

## Rename or merge products

A rename updates the displayed product name when it previously matched the identifier. A merge additionally requires an existing target with matching stock unit, stock-maintenance status, serial and batch flags, and variant parent. Template products cannot merge. Reject two active bundle definitions for the merging products, or two separate lead-time records. Also reject a merged result that would give the same product/warehouse multiple submitted rows on one stock reconciliation. A reconciliation expresses a target balance, so summing its target rows would invent stock.

For an admissible merge, update references to the surviving product, reconcile overlapping warehouse balance records, restore the latest purchase rate and recalculate affected warehouse quantities, valuation and active reservations. Warehouse planning balances can exist without stock movement and still need to survive the merge. Use the revised identities consistently in reports and pending purchasing or manufacturing demand.
