# Inventory and valuation

## Persistent model and conservation

Inventory is an ordered record of quantity changes and value changes for a product and warehouse within a company. A stock-ledger row records source document and source row, posting date and time, signed stock quantity, incoming or outgoing rate where applicable, quantity after transaction, valuation rate, stock value, stock-value difference and any serial, batch or inventory-dimension references. The warehouse balance is a derived current snapshot. It is not a replacement for historical ledger entries.

For a normal movement, next quantity equals previous quantity plus signed movement quantity. Next inventory value follows the chosen valuation method. Stock-value difference equals rounded next inventory value minus the previously carried inventory value. When quantity becomes exactly zero, inventory value is forced to zero. A count reconciliation can instead set an absolute target quantity and value; it must not be interpreted as an ordinary additional receipt of that target quantity.

Transaction creation time and business posting time have different meanings. Late entry of a transaction with an earlier posting time can change subsequent valuations, transfer values and financial postings. Reposting is current operational behavior needed for backdated corrections; it is not data migration and remains in scope.

Evidence: source-artifact-9dde27288d6d3f0994cd lines 1005–1215.

## Four supported valuation methods

The current snapshot supports moving average, first in first out, last in first out, and standard cost. They make different financial decisions and must not be collapsed into a single average. Selected serial or batch valuation paths also affect which actual costs are attached to movements. Standard cost takes precedence over serial or batch cost valuation for the monetary carrying amount while identity tracking still matters.

| Method | Ordinary receipt | Ordinary issue | Persisted valuation state |
|---|---|---|---|
| Moving average | Recalculate weighted value when prior stock is positive | Usually retain current average | Balance quantity, carried value and rate |
| First in first out | Append or merge newest cost layer | Consume earliest layer, subject to explicit-rate selection | Ordered remaining quantity and rate layers |
| Last in first out | Append or merge newest cost layer | Consume latest layer | Ordered remaining quantity and rate layers |
| Standard cost | Carry at effective approved standard rate | Carry at effective approved standard rate | Effective dated standard and on-hand value |

Evidence: source-artifact-09b661db83d498d60156 lines 16–267; source-artifact-9dde27288d6d3f0994cd lines 1716–1804; source-artifact-9dde27288d6d3f0994cd lines 1005–1215; source-artifact-88fa2add755bfc5588cb lines 32–314.

## Moving average: precise branches

Let previous quantity be positive ten, previous rate four, and incoming quantity five at rate seven. Previous value is forty. Next quantity is fifteen, next value is seventy-five, and next rate is five. For a later ordinary issue of six with no overriding outgoing rate, next quantity is nine, value forty-five, and expense value thirty.

The general positive-stock receipt formula is `(previous quantity × previous rate + incoming quantity × incoming rate) ÷ next quantity`. If the previous quantity is zero or negative and a positive receipt makes the next quantity nonnegative, the inspected method uses the incoming rate directly. It does not blend a fictitious negative inventory value with the new receipt as though that represented physical stock acquired at the old cost.

An issue carrying an explicit outgoing rate can change the rate of the remainder. When the resulting quantity is nonzero, the new rate is `(previous quantity × previous rate + signed issue quantity × outgoing rate) ÷ next quantity`. When it becomes zero, the outgoing rate is retained as rate state, while value is zero. This matters for purchase returns with a historical cost different from the current average. For ten units at average five, returning two at seven leaves eight units valued at thirty-six, or 4.5 each.

If the next quantity is negative, crossing from nonnegative stock with an explicit outgoing rate adopts that outgoing rate. A missing valuation rate can be supplied by an incoming rate or a fallback lookup unless zero valuation is expressly allowed. The exact fallback hierarchy is not fully specified by this paragraph; it must be matched to the separate transaction's valuation-rate contract.

The ledger rounds stock value to company currency precision and quantity to its configured quantity precision. For a nonzero moving-average balance, it recalculates the rate using rounded value divided by rounded quantity before persisting the final value. Do not assume that rate always has two decimal places or round it before multiplying by a large quantity.

Evidence: source-artifact-9dde27288d6d3f0994cd lines 1716–1804; source-artifact-9dde27288d6d3f0994cd lines 1005–1215.

## Ordered cost layers

A layer holds remaining quantity and per-stock-unit rate. A receipt at the same rate as the last layer merges into that layer; otherwise it appends when the last layer is positive. On a first in first out issue, an explicitly positive outgoing rate, or a purchase-return flag, first searches for a layer with exactly the requested rate. If none matches, consumption starts at the earliest layer. Ordinary issues start at the earliest layer. Last in first out consumption always starts with the latest layer; its outgoing-rate argument does not select a matching existing layer.

Receive ten units at four and five units at seven. Issuing twelve under first in first out consumes forty plus fourteen, leaving three units at seven with value twenty-one. Issuing twelve under last in first out consumes thirty-five plus twenty-eight, leaving three at four with value twelve. Both finish with quantity three but recognise different issue costs. A replacement that compares only quantity would miss this difference.

When stock is exhausted and an allowed issue still has quantity remaining, the layer state retains a negative layer priced from the supplied outgoing rate or the exhausted layer. A new receipt that only reduces the negative layer retains its old rate; a receipt that makes the layer positive replaces the remaining layer with the incoming rate. These branches are directly exercised in the inspected valuation tests. Near-zero layer quantities and totals with absolute magnitude strictly below one ten-millionth are normalised to zero. A value exactly at that threshold is not covered by the strict less-than normalisation.

Evidence: source-artifact-09b661db83d498d60156 lines 16–267; source-artifact-60fc0d3219f1096c48b2 lines 16–206.

## Standard cost and effective dating

A standard cost record binds product, company, effective date and positive standard rate. The effective rate is selected for the posting date. A missing effective standard rate prevents a stock posting. The first standard must be established before any stock ledger activity exists for the product and company. Effective dates cannot be in the future, must strictly increase, and a rate change cannot precede the latest stock activity date. Receipts and issues use the standard, even if purchasing price or consumed manufacturing cost differs. Ten units received with transaction rate 150 and standard rate 100 carry stock value 1,000, not 1,500.

A later standard-rate change revalues existing stock through a submitted revaluation document. Ten units changing from standard 100 to standard 130 become worth 1,300 without a quantity change. New stock transactions cannot be dated before the latest submitted standard's effective date. This protects the on-hand snapshot used at revaluation. Cancellation of a rate is constrained by stock activity from its effective date and reverses associated revaluation where permitted.

Purchase price variance and manufacturing variance are distinct accounting effects. Receiving one unit at purchase value 200 with standard value 130 produces seventy of purchase price variance. A later invoice without stock update clears received-but-not-billed at 200 and does not book another seventy of variance. Consuming five units at standard fifty and adding thirty of operating cost to produce one finished unit at standard 200 produces eighty of manufacturing variance. The finished inventory remains at 200; the variance must not be misclassified as a generic stock adjustment. These numeric outcomes are present in inspected source test definitions, which have not been executed during this review.

Evidence: source-artifact-9dde27288d6d3f0994cd lines 57–102; source-artifact-88fa2add755bfc5588cb lines 32–314; source-artifact-246cf4f12ac2a5d0bc90 lines 144–184; source-artifact-246cf4f12ac2a5d0bc90 lines 496–590; source-artifact-246cf4f12ac2a5d0bc90 lines 744–825.

## Reservations, projected stock and availability

Projected quantity is actual quantity plus purchase-ordered quantity plus requested quantity plus planned production quantity, less sales demand reservation, production material reservation, subcontract material reservation and production-plan reservation. These are planning counters. An explicit stock reservation is a separate claim on physical stock and is not another term subtracted from that planning formula.

Available quantity to reserve is actual stock less unconsumed active explicit reservations. Remaining claim for a reservation is reserved quantity minus delivered quantity minus transferred quantity minus consumed quantity. To reserve against a source row, the maximum is the smaller of warehouse availability and source required quantity minus already delivered stock quantity minus reservations against the same row. Sales delivered quantity is converted using the source conversion factor before this comparison. Both candidate and permitted quantity are rounded to reservation field precision.

The availability read and reservation write must be protected against concurrent reservations, including when no reservation exists yet for that product and warehouse. A check followed by an unprotected write is not equivalent: two users could each reserve the same final ten units. The inspected source explicitly serialises the relevant balance and reservation records. A replacement can choose any mechanism that preserves the same exclusion outcome.

Reservation state distinguishes Draft, Partially Reserved, Reserved, Partially Delivered, Delivered, Partially Used, Closed and Cancelled. Transferred quantity takes precedence in determining Closed or Partially Used. Otherwise an exact match between reserved quantity and delivered quantity, or consumed quantity when delivered quantity is empty, determines Delivered. Records already partially or fully delivered, created from a pick list, or carrying positive delivered quantity cannot be freely edited through the inspected update path. Cancellation and a new reservation are separate operations with traceable consequences.

Evidence: source-artifact-f3019fa86bf90715e1a7 lines 40–94; source-artifact-b1dc48719460ed10d39e lines 563–690; source-artifact-b1dc48719460ed10d39e lines 726–781.

## Serial and batch allocations

The current allocation model groups entries in a serial-and-batch allocation document linked to a source transaction row. Entries carry product identity, warehouse, serial identity or batch identity, quantity and value. Direction determines the sign. Serial entries normalise an absolute quantity above one to one. Outward allocations carry negative quantities and values. Aggregate bundle quantity must agree with the transaction's applicable stock quantity; after field-precision rounding, an absolute mismatch greater than 0.01 fails. Stock movements use transfer quantity, invoices use stock quantity, and supplied subcontract materials use consumed quantity.

Serial identity validation and batch balance validation are distinct. Do not assume that enabling ordinary product negative stock permits an absent serial identity. Conversely, this snapshot explicitly permits negative **batch** stock when allowed on the batch or in stock settings. The documentation must preserve that setting rather than impose a universal prohibition copied from older behavior. A positive batch-level permission suffices; otherwise the global batch permission is consulted. Policy evidence: source-artifact-cdd32f3c45fe4b1e3b6d lines 2346–2356.

For outward serialized stock, each selected identity must be available in the specified warehouse. An identity reserved to another document is rejected with a distinct reservation explanation. Inward identities cannot already be on hand in a warehouse under the applicable submission validation; manufacture and repack also reject identities already marked delivered. These are ownership checks, not numerical inventory tolerances. Serial selection uses creation order by default, reverses it for last in first out selection, and can use service-coverage expiry for expiry selection. Claims for the current document can restrict selection to its reserved identities; claims for other documents and identities already used in the current draft are excluded. Posting-time-aware selection reconstructs eligible historical identities, rather than assuming the current warehouse field is the complete historical answer. Evidence: source-artifact-cdd32f3c45fe4b1e3b6d lines 269–388; source-artifact-cdd32f3c45fe4b1e3b6d lines 2489–2580.

Batch availability combines available stock, stock-ledger adjustments, retail invoice claims, explicit reservations and pick-list claims. Expiry ordering places batches without an expiry after dated batches. Unless a negative-batch inspection is requested, only quantities positive at stock quantity precision remain. In the explicitly selected-batch filter reviewed here, expiry on or after the current business date is eligible and an absent expiry is eligible; it does not use the backdated movement date in that particular helper. Alternative batch lookup paths and historical posting eligibility still require dedicated reference scenarios before asserting one universal expiry-date policy. Evidence: source-artifact-cdd32f3c45fe4b1e3b6d lines 2638–2651; source-artifact-cdd32f3c45fe4b1e3b6d lines 3052–3102.

The ordinary negative-stock guard evaluates previous quantity plus signed movement less protected reservation, rounded to configured quantity precision. It rejects a negative result only when its magnitude exceeds 0.0001 for precision up to four, or one unit in the last decimal place for finer precision. The comparisons are strict. Replacing these conditions with an unrounded mathematical less-than-zero test changes acceptance at small boundaries. Evidence: source-artifact-9dde27288d6d3f0994cd lines 1387–1406.

Evidence: source-artifact-cdd32f3c45fe4b1e3b6d lines 671–684; source-artifact-cdd32f3c45fe4b1e3b6d lines 1189–1215; source-artifact-cdd32f3c45fe4b1e3b6d lines 1696–1725.

## Landed cost allocation

Landed costs capitalise additional attributable charges into received stock. Total charges are summed in company currency. Automatic allocation distributes them using the chosen row quantity or amount basis. For row basis `basis`, allocate `total charges × basis ÷ sum of bases`, round each allocated amount to its field precision, then put the residual on the final row so the allocation reconciles exactly. A zero total basis fails; the system does not invent equal allocation when an amount basis is zero.

Manual distribution must reconcile to total charges. The difference is rounded to the applicable currency precision; when its absolute value is less than two smallest currency units it is absorbed into the last row, otherwise the allocation fails. At two decimal places, a rounded difference of 0.01 can be corrected while 0.02 fails. Charges of ten split equally among three rows at two decimal places become 3.33, 3.33 and 3.34. Allocation order is therefore financially observable.

Landed cost after consumption can alter historical incoming cost and downstream issue cost. Update stock valuation, dependent transfers and accounting together through the reposting workflow; merely increasing the current warehouse value leaves earlier cost of sales incorrect. Allocation is distinct from the vendor invoice that incurs the freight or other charge; prevent both omission and double capitalisation.

Evidence: source-artifact-0384b50b0a0419065d6e lines 304–371. The reposting dependency paths are inventory-ledger behavior; transaction-specific charge-account composition requires the accounting-domain contract.

## Acceptance and verification boundaries

Acceptance must compare quantities, inventory values, stock-value differences, ledger debit and credit effects, reservation remainder and serial or batch ownership after every operation. Include normal receipt, partial issue, full issue, zero-value receipt, explicit-rate purchase return, negative-stock transition, backdated receipt, landed cost after delivery, standard revaluation, cancellation, and repeating the same attempted posting after a failure. Document operations must either leave all required effects or leave none.

The reviewed arithmetic establishes the worked examples and branch conditions above. Complete runtime proof still requires the full transaction suites with company precision settings, inventory dimensions, inter-company transfers, serial-specific valuation and concurrent posting. A claim that every inventory behavior has been dynamically validated would exceed the evidence recorded here.
