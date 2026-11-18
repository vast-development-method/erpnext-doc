# Inventory decisions at the voucher boundary

A voucher line can affect quantity, valuation, account balances, reservations, tracking and inspection independently. Each rule gives the condition that selects the operation and an observable example.

## Warn on zero valuation

Inspect items in point-of-sale, purchase or sales invoices, delivery notes, purchase receipts, stock entries and stock reconciliations.

A zero valuation rate qualifies directly. A zero incoming rate qualifies when stock updates are enabled, defaulting to enabled when the switch is absent.

If zero valuation is explicitly disabled on the row and the item master identifies a stock item, display an orange warning naming the row and translated allowance label. Continue processing.

**Example.** On a purchase receipt, a stock item at valuation rate zero and allowance 0 raises a warning. An allowance of 1 suppresses it.

## Validate item identities

An empty item table completes immediately. Collect item codes and fetch the existing master names in a single membership query.

Compute the distinct missing names. If any remain, fail validation with their names; their display order is unspecified.

**Example.** Rows A, B, B against master A fail with one missing code, B.

## Merge inventory-account assignments

Build a fresh map. Visit ordinary items, packed items and supplied items in that order, skipping empty tables.

Pass each populated table and the company to the item account resolver. Merge returned entries into the result, with later tables replacing an earlier mapping for the same key. Return the combined map.

**Example.** A key present in both items and supplied items uses the supplied-items mapping in the returned map.

## Choose the company's inventory-account basis

Read the company-level enable-item-wise-inventory-account flag using the cached Company record. Return its stored value to callers choosing the lookup basis.

**Example.** An enabled flag for company A selects the per-item route whenever the requesting operation queries A. Company B supplies its own flag.

## Resolve the inventory account and its currency

Normalize a mapping row to allow field lookup. With item-based accounts enabled, prefer a nonempty raw-material code to the ordinary item code and return that code’s mapped account. An absent item account raises a configuration error even when the optional warehouse lookup flag is false.

Otherwise select the requested warehouse field, defaulting to warehouse. Prefer the row value, falling back to the document field. If both are empty return the initially empty account structure.

Look up the warehouse mapping. On a miss with account derivation enabled, derive the warehouse account, fetch its currency, cache both under the warehouse and return them. A miss with account derivation disabled returns the lookup miss.

**Example.** With a warehouse account map initially empty, a warehouse resolving to Stock EUR yields that account and its stored currency and fills the cache for subsequent rows.

## Select item or warehouse accounts

Read the company’s item-account switch. When enabled, obtain the merged document item inventory account map. Otherwise request the company warehouse-to-account map. Return the selected result.

**Example.** With warehouse accounting enabled through the item-account switch being off, two items at the same warehouse look up the same warehouse key.

## Recognise stock and provisional journals

For cancelled documents first request reversal by voucher type and number. Read the company’s provisional non-stock setting, detect any fixed-asset row, and determine whether stock or packed items exist under perpetual inventory.

Load the inventory account map only for that last condition. Continue toward posting if any of the three conditions is true. Only a submitted document enters the forward posting branch.

Use a supplied nonempty journal list directly. Otherwise generate voucher-specific legs, giving a purchase receipt the landed-cost flag along with its account map, and other types only the map. Forward the legs and repost flag to the posting service.

**Example.** A submitted purchase receipt containing only a fixed asset can enter the journal path with an empty inventory map. A cancelled receipt requests reversal and creates no forward journal through this branch.

## Capture serial and lot numbers from row input

Skip updates after submission. Use the requested row table or items by default, and use stock item rows for Asset Capitalization. Inspect only serial- or batch-tracked items.

When a bundle and direct serial and batch values coexist, check them for consistency except during landed-cost reposting. Presence of a directly entered value enables the row’s direct-entry flag.

For rows still lacking both ordinary and rejected bundles, build new bundles from the voucher identity, row, posting timestamp, company and actual stock movement. Separate accepted and rejected quantities. A non-return internal transfer with a source warehouse creates its outward bundle there. The normal path requests draft bundles; landed-cost reprocessing changes that flag.

**Example.** On a purchase receipt with four accepted batch-tracked units and one rejected unit, legacy batch input and no existing bundles, expect distinct links for the normal and rejected movement, against their respective warehouses.

## Recover identities and costs on return

Run for return vouchers. Resolve original row references for eligible tracked items, then filter the available serial/batch entries to the return row. Packed components use the parent detail and item identity.

Store the recovered bundle and clear the direct batch and serial fields. Sales Invoice and Delivery Note return rows take their incoming rate from the recovered bundle’s average rate.

Purchase Receipt and Purchase Invoice returns also recover rejected quantities. The return-from-rejected-warehouse flag selects the row quantity, warehouse and ordinary bundle field for that case. A matched rejected availability row with zero available stock raises an error.

**Example.** Return one previously delivered serial from a Delivery Note. The return row gets its own bundle based on the referenced original detail and its incoming rate becomes the new bundle’s average rate.

## Enable direct serial and lot entry

Read the Stock Settings switch for direct serial and batch fields. When enabled, mark every main item row as using those fields. When disabled the operation leaves existing row values alone.

**Example.** Two main items with their flags unset both become marked when the site switch is enabled. An already marked row stays marked if this operation subsequently runs with the switch off.

## Balance stock-value changes across accounts

Read the voucher’s stock ledger grouped by line and its inventory-account mapping. Each mapped stock value difference produces equal and opposite amounts on inventory and the expense/difference account, or the target warehouse inventory account when the detail has a target warehouse.

Carry cost center, project and opening status into the postings. For an internal transfer, a residual whose absolute amount exceeds one unit of the general ledger precision produces a rounding gain/loss pair. A company warehouse with no resolvable inventory account raises an error.

Return the processed journal lines. This composes lines; ledger insertion belongs to the posting path.

**Example.** For one receipt row with a positive stock value difference of 120 and a valid expense/difference account, expect an inventory debit of 120 and the offsetting credit of 120 after normalizing the signed lines.

## Identify affected items and warehouses

Combine main and packed rows. Collect each nonblank item code and ordinary warehouse once. Stock Entry additionally includes source and target warehouses. Return two lists built from sets, so callers must treat their order as unspecified.

**Example.** A Stock Entry transfers item A from WEST to EAST on two rows. The affected sets contain one item, A, and two warehouses, WEST and EAST.

## Group active movements by voucher line

Read uncancelled Stock Ledger Entries for the exact voucher type and name. Return a map from voucher detail ID to all matching entries, retaining entry ID, warehouse, item, posting date/time, value change, valuation rate, movement, resulting quantity and project.

**Example.** A transfer detail with an active source entry and an active destination entry has two elements under the same detail key. A cancelled entry for that detail is excluded.

## Cancel tracking allocations

Visit items, packed item rows and supplied item rows. Clear the row batch number; where an ordinary bundle is linked, flag the bundle and its entries as cancelled and clear the link.

For main items also cancel and unlink a rejected bundle. Clear a linked current bundle reference when present. The cancellation preserves the batch master and updates its movement links.

**Example.** A main receipt item linked to accepted bundle OK1 and rejected bundle RJ1 loses both links. Both bundles and their child entries acquire cancellation flags.

## Synchronise tracked quantities with their voucher line

Walk the requested table, defaulting to items. For each populated ordinary, current or rejected bundle link, synchronize that bundle to the voucher and row using quantity, previously recorded quantity or rejected quantity respectively. All three links follow the same synchronisation rule.

**Example.** On a reconciliation detail with an ordinary bundle for proposed quantity 5 and a current bundle for quantity 4, synchronise each against its corresponding field. A rejected bundle on a purchase row instead uses rejected quantity.

## Create the receiving allocation for a transfer

Copy the input bundle for the target warehouse, default the movement direction to Inward and attach the voucher identity. New or cancelled vouchers leave the copied voucher number blank.

Reset cancellation, set each child warehouse and voucher linkage, normalize quantities and stock value differences to the requested direction and recalculate. A single non-serial entry can use a smaller nonzero requested quantity. Save as draft when requested, otherwise submit, and return the new bundle name.

**Example.** Copy a single-batch inward bundle of ten units to warehouse B with requested quantity four and draft mode. The new bundle is a separate draft with one positive four-unit entry in B.

## Build a signed inventory movement

Construct a candidate Stock Ledger Entry with voucher and detail identifiers, posting timestamp, company fiscal year, stock unit, warehouse, bundle and row-or-parent project. The default quantity sign is positive on submitted documents and negative otherwise. Cancelled vouchers carry the cancellation marker.

Apply caller overrides before evaluating inventory dimensions. The rejected warehouse on a purchase picks rejected dimension fields. A positive Stock Entry movement into its target warehouse can take the destination dimension. During cancellation copy populated direct serial and batch fields for older records.

**Example.** A submitted transfer detail has stock quantity 6 and destination bin B-2. For its incoming leg pass the target warehouse and actual quantity +6; evaluate the destination dimension on that final leg. Build the outgoing leg separately with its own warehouse and quantity.

## Apportion landed cost across accounts and dimensions

Return early when there is no landed-cost amount or no submitted receipt relation. For each linked landed-cost voucher, compute the total allocation basis across its items. Manual distribution uses applicable charges; other modes use the chosen basis field.

For the current receipt allocate each charge row’s account and base currency amounts proportionally to that basis. Group by item code and receipt detail, then by expense account and full dimension values. Identical accounts with different dimensions remain separate.

**Example.** Two items have allocation bases of 1 and 3. A freight charge of 40 in account currency and 80 in company currency allocates 10 and 20 to the first item, 30 and 60 to the second. A separate freight tax row with different dimensions remains separately identifiable.

## Apply stock and batch consequences

Send the candidate entries and the negative-stock and landed-cost flags to the inventory posting operation. Update batch quantities for the voucher type, name and document status with the same landed-cost context, then validate outstanding batch reservations.

**Example.** After a Delivery Note issues two units from a batch, check both the batch balance and reservations. If the balance left in that warehouse cannot cover another order’s outstanding reservation, the validation must interrupt the posting transaction.

## Reverse the financial consequences of cancellation

Except during a repost, cancel the linked exchange gain/loss journal for this voucher.

Look for at least one general-ledger entry with this voucher type and number. If present, invoke the voucher’s general-ledger posting operation, which selects reversal for a cancelled voucher.

**Example.** A cancelled voucher with existing ledger entries and valuation reprocessing enabled invokes the voucher posting operation and skips exchange gain/loss cancellation.

## Validate source and destination warehouses

Read ordinary item rows. Gather distinct nonempty warehouse values separately for warehouse, target warehouse and from warehouse.

Concatenate those three groups. Validate each warehouse for disabled status and then company ownership; propagate failure. The same warehouse may be checked in more than one group.

**Example.** If a transfer’s source belongs to the voucher company but its target belongs to another company, target validation fails.

## Recalculate the billed proportion

Use the voucher’s item line collection. Identify the parent by its voucher identity and use the reference amount and billed amount to calculate the parent percentage billed.

For a delivery note compute and supply its specialized billing percentage. Invoke the shared percent-field updater with the original update-modified flag.

**Example.** A delivery note requests the delivery-specific quantity/amount calculation; another supported voucher uses the generic amount mapping.

## Recognise delivery billing by amount and quantity

Fetch invoiced quantities by delivery item and freshly persisted delivery rows. Prefer open rows, falling back to all if all are closed.

Sum amount and returned quantity times rate. If aggregate returns meet or exceed the aggregate amount, use original row amounts; otherwise subtract each row’s returned amount. Use absolute reference amounts and skip zero references.

For each row, take the larger of (a) the absolute billed amount capped at its reference and (b) reference times the lesser of 1 and invoiced quantity divided by net quantity. The quantity contribution is zero when net quantity is zero.

Accumulate both bases and return 100 times total recognized divided by total reference, rounded to six decimal places. A zero reference total yields zero.

**Example.** A delivery line of 10 units at 10, with all 10 invoiced for 80 after a price reduction, reaches 100 percent. With only 6 invoiced for 60 it reaches 60 percent.

## Distribute invoiced quantities to delivery lines

Start with quantities billed directly against this delivery note. Read the set of distinct nonempty sales-order line references in the note.

For each, update the map with the quantities distributed by the sales-order billing helper. Matching keys are replaced by that result. Return the combined map.

**Example.** Two delivery rows referring to the same order line trigger one sales-order allocation lookup. Its mapped quantity replaces a direct quantity under the same delivery-row key.

## Enforce the inspection policy

Restrict invoice checks to invoices that update stock. For purchases and deliveries read the relevant per-item inspection requirement. Stock Entries require their own inspection switch and use the purpose and row direction; Manufacture checks the finished item. Exempt secondary rows under the stated purpose rules.

For supported purchases and deliveries, a site setting can defer inspection. Otherwise missing required inspection warns while saving and blocks submission. At submission, separately handle a linked unsubmitted or rejected inspection using the respective Stop-or-warn setting.

**Example.** With deferred inspections disabled, save a delivery draft containing an item that requires inspection but has none. Expect a warning at save and a refusal at submit. If a rejected inspection is linked, the rejection setting controls whether submission is blocked or warned.

## Refresh blanket-order commitments

Collect distinct, nonempty blanket order references from ordinary item rows. Load each referenced blanket order and invoke its ordered-quantity recalculation once.

**Example.** Three lines referring to A, A and B cause two blanket-order recalculations.

## Permit zero valuation for customer-owned goods

Look up the cached customer-provided flag for each ordinary item. On a true flag set the row’s zero-valuation allowance to 1. Other rows keep their current value.

**Example.** With customer-provided part C and ordinary part D, both initially disallowing zero valuation, only C becomes eligible.

## Calculate the price per stock unit

Apply to purchase receipts, purchase invoices and orders, sales invoices and orders, delivery notes and quotations. For each item divide the commercial line rate by the conversion factor, substituting 1 when the factor is absent or zero. Store the result as rate per stock unit.

**Example.** A case at 120 with 12 stock units per case gives 10 per stock unit. With conversion factor zero, the row keeps 120 as the stock-unit rate.

## Schedule forward valuation after a backdated change

Build a repost context with voucher, company, posting date/time and landed-cost indicator. Cancellation forces a repost decision. Otherwise create work only when forced, when future stock entries exist, or when the queue rule requires it.

Choose item/warehouse-based reposting or one voucher-based valuation repost according to Stock Reposting Settings. This schedules valuation work; it does not demonstrate that a worker has completed the recalculation.

**Example.** Backdate a receipt before a later stock issue. With future ledger entries present and voucher-based reposting selected, expect a valuation repost for the receipt. Check completion before comparing the later issue’s revised stock and general ledger amounts.

## Carry currency and dimensions onto a posting

Create a line with account, cost center, debit, credit, opposing account and remarks. Attach supplied project, voucher detail, posting date and nonzero explicit account-currency amounts.

Apply explicit dimension values to the arguments passed into the shared general ledger builder, overriding derived values. Append one built line to the requesting operation’s list; this operation does not create the counter-entry or commit a journal.

**Example.** Append a debit of NAD 120 in the company books with EUR 6 in the account currency. Pass a project and a branch dimension override. The resulting candidate retains those explicit fields and the requesting operation must build its balancing credit separately.

## Apply or reverse subcontract reservations

Process subcontracting deliveries, sends to subcontractor whose order reserves stock, and non-return subcontracting receipts with reserved stock. Resolve the row table, related voucher and target counter from the mapping.

For each eligible row, load submitted reservation identifiers in creation order. Use transfer quantity when present, otherwise consumed quantity. Skip rows with no matching reservation and stop when quantity is exhausted.

For serial-based reservations, mark matching child serials delivered on submit or undelivered otherwise; count each match once per local list. For batch-based reservations, negate bundle quantities, cap each matched child by available or delivered quantity, then persist the child.

Ordinary reservations take the smaller of the remaining row quantity and available reserved quantity (submit) or already applied counter (reverse). Increase or decrease the chosen reservation counter, persist it, refresh reserved quantity on the voucher, reservation status and warehouse bin, then reduce the remainder.

**Example.** Submitting 5 untracked units against successive eligible reservations with headroom 3 and 4 increments the first by 3 and the second by 2. Both reservations refresh their voucher and bin quantities.

## Select reservations eligible for the movement

Within the current reservation-update row, select submitted Stock Reservation Entry records whose voucher type matches the purpose mapping. Match its configured voucher number, taking the row subcontracting order only when that mapping has no voucher-number key.

With a detail reference field, compare the reservation’s voucher-detail number with that row field. Otherwise match raw material code and the document’s supplier warehouse. Return reservation names in ascending creation order.

**Example.** A subcontracting receipt for material RM at supplier warehouse W selects submitted reservations for that order, RM and W, oldest first.

## Select the subcontracting reservation counter

For Subcontracting Delivery use items, a Subcontracting Inward Order from the document, its inward subcontract order line row reference and delivered quantity.

For Send to Subcontractor use items, a Subcontracting Order from the document, its subcontract order material line reference and transferred quantity.

For Subcontracting Receipt use supplied item rows, a Subcontracting Order and consumed quantity; obtain order and raw material from the row through the selection operation.

**Example.** A send increments transferred quantity on the reservation. A receipt increments consumed quantity even when both relate to the same subcontracting order.

## Reject held and closed commitments

Keep eligible rows with a reference and without the requested exclusion flag. If none remain complete without querying. Fetch statuses for their distinct reference identifiers.

In the original eligible order inspect each identifier once. Collect one translated message per Closed or On Hold reference. Other or missing status values yield no message here.

Raise one invalid-status error containing all collected messages if any are present.

**Example.** Rows referencing a held A twice and a closed B once raise one combined error containing A and B once each.

## Select eligible commitment references

Evaluate the selected row reference field. An empty reference is empty or false; a populated reference qualifies unless an exclusion field was configured and its row value is set. The commitment reference and exclusion flag are selected for the transaction type.

**Example.** An item with purchase order A and exclusion flag 1 is skipped when that exclusion field is configured.

## Preview financial postings

Accept company, voucher type and voucher name. Prepare a company filter with dimensions enabled, retrieve the voucher and require read permission.

Invoke the configured financial-preview preparation, compute accounting columns and rows, then roll back the database transaction before returning those two arrays under column definitions and journal rows.

**Example.** A permitted reader receives ledger dimensions in the accounting preview and the preview’s transaction is rolled back. A failed read check prevents computation.

## Preview inventory movements

Accept company and voucher identity. Select currency formatting for valuation, retrieve the voucher and require read permission.

Invoke the configured inventory-preview preparation, obtain the stock columns and rows, roll back the transaction and return them under column definitions and inventory rows.

**Example.** A warehouse voucher preview returns stock rows with currency-valued valuation and leaves preview writes rolled back.

## Determine whether outgoing cost layers need recalculation

Select this voucher’s uncancelled stock-ledger rows with negative actual quantity. Build ordered item/warehouse pairs.

If every pair is distinct, return false. Otherwise return true if any selected row’s stock queue differs from the stored representation of an empty layer list, even if that row belongs to a different pair. Return false if all equal the stored empty layer list.

**Example.** Two outgoing A/W entries with empty queues plus one outgoing B/W entry with a populated queue return true; three distinct pairs return false regardless of queue contents.

## Select item rows needing inspection

Parse rows and resolve the inspection flag for this voucher type. Without a mapping return all rows for Stock Entry and an empty list for other unmapped types.

For a mapped submitted document whose site permits inspection after purchase or delivery, return the input rows. Otherwise query distinct item codes for the relevant master flag and return qualifying original rows in input order with duplicates preserved.

**Example.** For flagged A and unflagged B, a draft containing A, B, A returns A, A; an eligible submitted voucher with post-transaction inspection enabled returns all three.

## Create inspection records

Accept an authorised inspection-creation command with its item lines. For each item reject sample size greater than accepted quantity using numeric conversions.

Build and save an inspection for the passed company, inspection type and reference voucher. Set inspector to the session user and preserve item code, description, numeric sample size, batch and child-row reference. Use only the first newline-delimited serial when provided.

Return the saved inspection identifiers in input order. Individual inspections share the transaction boundary of the command.

**Example.** For an accepted quantity of 5, sample 2 and serials S1 then S2 on separate lines, the new inspection records sample 2 and S1. A sample of 6 raises validation failure.

## Identify outstanding valuation work

Query for the existence of a submitted Repost Item Valuation record whose status is Queued or In Progress. A qualifying record identifier is sufficient to establish that work is pending.

**Example.** A completed submitted repost and a draft queued repost alone leave this check empty or false. A submitted queued repost makes it set.

## Invalidate a prior decision about later movements

If the current execution context carries a future-stock-ledger cache, remove the entry keyed by the exact pair of voucher type and number. Missing keys or a missing cache are tolerated.

**Example.** Evicting Delivery Note / A keeps Stock Entry / A cached. Repeating the eviction completes without error.
