# Inventory and valuation

## Internal contracts

| Record family | Persistent contract and responsibility |
|---|---|
| Movement and current balance | [Inventory movement](../../schemas/data/record-types/stock_ledger_entry.json) preserves each valuation consequence; [warehouse balance](../../schemas/data/record-types/bin.json) stores recalculable planning and on-hand counters |
| Movement authority | [Stock movement](../../schemas/data/record-types/stock_entry.json) and [movement row](../../schemas/data/record-types/stock_entry_detail.json) bind signed quantities to a business purpose and warehouse pair |
| Tracking allocation | [Allocation document](../../schemas/data/record-types/serial_and_batch_bundle.json), [allocation entry](../../schemas/data/record-types/serial_and_batch_entry.json), [serial identity](../../schemas/data/record-types/serial_no.json) and [batch](../../schemas/data/record-types/batch.json) preserve custody independently of aggregate cost |
| Physical commitment | [Stock reservation](../../schemas/data/record-types/stock_reservation_entry.json) records claim, source row, fulfilment and release |
| Cost adjustment | [Standard cost](../../schemas/data/record-types/item_standard_cost.json), [landed cost](../../schemas/data/record-types/landed_cost_voucher.json) and [revaluation work](../../schemas/data/record-types/repost_item_valuation.json) preserve the authorisation and progress of recalculation |
| Mathematical and acceptance contracts | [Inventory calculations](../../schemas/mathematics/inventory-calculations.json) define operands and precision; [inventory acceptance cases](../../schemas/mathematics/inventory-acceptance-cases.json) define complete inputs, operation order and expected balances |

The [financial accounting contract](financial-accounting.md) defines balanced postings and period controls. [Products, units and packaging](products-units-and-packaging.md) defines commercial-to-stock conversions. Any quantity compared in this chapter must already be in the same product stock unit. Monetary inventory values are in company currency, even when the purchasing document uses another currency.

## Persistent model and conservation

Inventory is an ordered record of quantity changes and value changes for a product and warehouse within a company. A stock-ledger row records source document and source row, posting date and time, signed stock quantity, incoming or outgoing rate where applicable, quantity after transaction, valuation rate, stock value, stock-value difference and any serial, batch or inventory-dimension references. The warehouse balance is a derived current snapshot. It is not a replacement for historical ledger entries.

For a normal movement, next quantity equals previous quantity plus signed movement quantity. Next inventory value follows the chosen valuation method. Stock-value difference equals rounded next inventory value minus the previously carried inventory value. When quantity becomes exactly zero, inventory value is forced to zero. A count reconciliation can instead set an absolute target quantity and value; it must not be interpreted as an ordinary additional receipt of that target quantity.

Transaction creation time and business posting time have different meanings. Late entry of a transaction with an earlier posting time can change subsequent valuations, transfer values and financial postings. Reposting is current operational behavior needed for backdated corrections; it is not data migration and remains in scope.

## Four supported valuation methods

The current snapshot supports moving average, first in first out, last in first out, and standard cost. They make different financial decisions and must not be collapsed into a single average. Selected serial or batch valuation paths also affect which actual costs are attached to movements. Standard cost takes precedence over serial or batch cost valuation for the monetary carrying amount while identity tracking still matters.

| Method | Ordinary receipt | Ordinary issue | Persisted valuation state |
|---|---|---|---|
| Moving average | Recalculate weighted value when prior stock is positive | Usually retain current average | Balance quantity, carried value and rate |
| First in first out | Append or merge newest cost layer | Consume earliest layer, subject to explicit-rate selection | Ordered remaining quantity and rate layers |
| Last in first out | Append or merge newest cost layer | Consume latest layer | Ordered remaining quantity and rate layers |
| Standard cost | Carry at effective approved standard rate | Carry at effective approved standard rate | Effective dated standard and on-hand value |

## Moving average: precise branches

Let previous quantity be positive ten, previous rate four, and incoming quantity five at rate seven. Previous value is forty. Next quantity is fifteen, next value is seventy-five, and next rate is five. For a later ordinary issue of six with no overriding outgoing rate, next quantity is nine, value forty-five, and expense value thirty.

The general positive-stock receipt formula is `(previous quantity × previous rate + incoming quantity × incoming rate) ÷ next quantity`. If the previous quantity is zero or negative and a positive receipt makes the next quantity nonnegative, the inspected method uses the incoming rate directly. It does not blend a fictitious negative inventory value with the new receipt as though that represented physical stock acquired at the old cost.

An issue carrying an explicit outgoing rate can change the rate of the remainder. When the resulting quantity is nonzero, the new rate is `(previous quantity × previous rate + signed issue quantity × outgoing rate) ÷ next quantity`. When it becomes zero, the outgoing rate is retained as rate state, while value is zero. This matters for purchase returns with a historical cost different from the current average. For ten units at average five, returning two at seven leaves eight units valued at thirty-six, or 4.5 each.

If the next quantity is negative, crossing from nonnegative stock with an explicit outgoing rate adopts that outgoing rate. A missing valuation rate can be supplied by an incoming rate or a fallback lookup unless zero valuation is expressly allowed. The ordered fallback contract below specifies the eligible balance, product and purchase-price inputs; explicit serial or batch valuation is resolved before that ordinary fallback.

The ledger rounds stock value to company currency precision and quantity to its configured quantity precision. For a nonzero moving-average balance, it recalculates the rate using rounded value divided by rounded quantity before persisting the final value. Do not assume that rate always has two decimal places or round it before multiplying by a large quantity.

## Ordered cost layers

A layer holds remaining quantity and per-stock-unit rate. A receipt at the same rate as the last layer merges into that layer; otherwise it appends when the last layer is positive. On a first in first out issue, an explicitly positive outgoing rate, or a purchase-return flag, first searches for a layer with exactly the requested rate. If none matches, consumption starts at the earliest layer. Ordinary issues start at the earliest layer. Last in first out consumption always starts with the latest layer; its outgoing-rate argument does not select a matching existing layer.

Receive ten units at four and five units at seven. Issuing twelve under first in first out consumes forty plus fourteen, leaving three units at seven with value twenty-one. Issuing twelve under last in first out consumes thirty-five plus twenty-eight, leaving three at four with value twelve. Both finish with quantity three but recognise different issue costs. A replacement that compares only quantity would miss this difference.

When stock is exhausted and an allowed issue still has quantity remaining, the layer state retains a negative layer priced from the supplied outgoing rate or the exhausted layer. A new receipt that only reduces the negative layer retains its old rate; a receipt that makes the layer positive replaces the remaining layer with the incoming rate. These branches are directly exercised in the inspected valuation tests. Near-zero layer quantities and totals with absolute magnitude strictly below one ten-millionth are normalised to zero. A value exactly at that threshold is not covered by the strict less-than normalisation.

## Standard cost and effective dating

A standard cost record binds product, company, effective date and positive standard rate. The effective rate is selected for the posting date. A missing effective standard rate prevents a stock posting. The first standard must be established before any stock ledger activity exists for the product and company. Effective dates cannot be in the future, must strictly increase, and a rate change cannot precede the latest stock activity date. Receipts and issues use the standard, even if purchasing price or consumed manufacturing cost differs. Ten units received with transaction rate 150 and standard rate 100 carry stock value 1,000, not 1,500.

A later standard-rate change revalues existing stock through a submitted revaluation document. Ten units changing from standard 100 to standard 130 become worth 1,300 without a quantity change. New stock transactions cannot be dated before the latest submitted standard's effective date. This protects the on-hand snapshot used at revaluation. Cancellation of a rate is constrained by stock activity from its effective date and reverses associated revaluation where permitted.

Purchase price variance and manufacturing variance are distinct accounting effects. Receiving one unit at purchase value 200 with standard value 130 produces seventy of purchase price variance. A later invoice without stock update clears received-but-not-billed at 200 and does not book another seventy of variance. Consuming five units at standard fifty and adding thirty of operating cost to produce one finished unit at standard 200 produces eighty of manufacturing variance. The finished inventory remains at 200; the variance must not be misclassified as a generic stock adjustment. These numeric outcomes are present in inspected source test definitions, which have not been executed during this review.

## Reservations, projected stock and availability

Projected quantity is actual quantity plus purchase-ordered quantity plus requested quantity plus planned production quantity, less sales demand reservation, production material reservation, subcontract material reservation and production-plan reservation. These are planning counters. An explicit stock reservation is a separate claim on physical stock and is not another term subtracted from that planning formula.

Available quantity to reserve is actual stock less unconsumed active explicit reservations. Remaining claim for a reservation is reserved quantity minus delivered quantity minus transferred quantity minus consumed quantity. To reserve against a source row, the maximum is the smaller of warehouse availability and source required quantity minus already delivered stock quantity minus reservations against the same row. Sales delivered quantity is converted using the source conversion factor before this comparison. Both candidate and permitted quantity are rounded to reservation field precision.

The availability read and reservation write must be protected against concurrent reservations, including when no reservation exists yet for that product and warehouse. A check followed by an unprotected write is not equivalent: two users could each reserve the same final ten units. The inspected source explicitly serialises the relevant balance and reservation records. A replacement can choose any mechanism that preserves the same exclusion outcome.

Reservation state distinguishes Draft, Partially Reserved, Reserved, Partially Delivered, Delivered, Partially Used, Closed and Cancelled. Transferred quantity takes precedence in determining Closed or Partially Used. Otherwise an exact match between reserved quantity and delivered quantity, or consumed quantity when delivered quantity is empty, determines Delivered. Records already partially or fully delivered, created from a pick list, or carrying positive delivered quantity cannot be freely edited through the inspected update path. Cancellation and a new reservation are separate operations with traceable consequences.

## Serial and batch allocations

The current allocation model groups entries in a serial-and-batch allocation document linked to a source transaction row. Entries carry product identity, warehouse, serial identity or batch identity, quantity and value. Direction determines the sign. Serial entries normalise an absolute quantity above one to one. Outward allocations carry negative quantities and values. Aggregate bundle quantity must agree with the transaction's applicable stock quantity; after field-precision rounding, an absolute mismatch greater than 0.01 fails. Stock movements use transfer quantity, invoices use stock quantity, and supplied subcontract materials use consumed quantity.

Serial identity validation and batch balance validation are distinct. Do not assume that enabling ordinary product negative stock permits an absent serial identity. Conversely, this snapshot explicitly permits negative **batch** stock when allowed on the batch or in stock settings. The documentation must preserve that setting rather than impose a universal prohibition copied from older behavior. A positive batch-level permission suffices; otherwise the global batch permission is consulted.

For outward serialized stock, each selected identity must be available in the specified warehouse. An identity reserved to another document is rejected with a distinct reservation explanation. Inward identities cannot already be on hand in a warehouse under the applicable submission validation; manufacture and repack also reject identities already marked delivered. These are ownership checks, not numerical inventory tolerances. Serial selection uses creation order by default, reverses it for last in first out selection, and can use service-coverage expiry for expiry selection. Claims for the current document can restrict selection to its reserved identities; claims for other documents and identities already used in the current draft are excluded. Posting-time-aware selection reconstructs eligible historical identities, rather than assuming the current warehouse field is the complete historical answer.

Batch availability combines available stock, stock-ledger adjustments, retail invoice claims, explicit reservations and pick-list claims. Expiry ordering places batches without an expiry after dated batches. Unless a negative-batch inspection is requested, only quantities positive at stock quantity precision remain. In the explicitly selected-batch filter reviewed here, expiry on or after the current business date is eligible and an absent expiry is eligible; it does not use the backdated movement date in that particular helper. Alternative batch lookup paths and historical posting eligibility still require dedicated reference scenarios before asserting one universal expiry-date policy.

The ordinary negative-stock guard evaluates previous quantity plus signed movement less protected reservation, rounded to configured quantity precision. It rejects a negative result only when its magnitude exceeds 0.0001 for precision up to four, or one unit in the last decimal place for finer precision. The comparisons are strict. Replacing these conditions with an unrounded mathematical less-than-zero test changes acceptance at small boundaries.

## Landed cost allocation

Landed costs capitalise additional attributable charges into received stock. Total charges are summed in company currency. Automatic allocation distributes them using the chosen row quantity or amount basis. For row basis `basis`, allocate `total charges × basis ÷ sum of bases`, round each allocated amount to its field precision, then put the residual on the final row so the allocation reconciles exactly. A zero total basis fails; the system does not invent equal allocation when an amount basis is zero.

Manual distribution must reconcile to total charges. The difference is rounded to the applicable currency precision; when its absolute value is less than two smallest currency units it is absorbed into the last row, otherwise the allocation fails. At two decimal places, a rounded difference of 0.01 can be corrected while 0.02 fails. Charges of ten split equally among three rows at two decimal places become 3.33, 3.33 and 3.34. Allocation order is therefore financially observable.

Landed cost after consumption can alter historical incoming cost and downstream issue cost. Update stock valuation, dependent transfers and accounting together through the reposting workflow; merely increasing the current warehouse value leaves earlier cost of sales incorrect. Allocation is distinct from the vendor invoice that incurs the freight or other charge; prevent both omission and double capitalisation.

The reposting dependency paths are inventory-ledger behavior; transaction-specific charge-account composition requires the accounting-domain contract.

## Posting procedure and account reconciliation

A stock posting is the following ordered business operation. These steps describe outcomes and sequencing, without choosing a persistence technology.

1. Resolve the submitted document and child row, company, warehouse, stock product, immutable stock conversion, posting date and time, valuation method, applicable dimensions, identity allocation and zero-value permission. Honour the document-specific predecessor-progress sequence: a purchase receipt updates purchase-order received progress before deriving the dependent warehouse planning counters, within the same atomic submission.
2. Serialise overlapping product-and-warehouse mutations. Acquire all required product-and-warehouse protections in a consistent sorted order, so two multi-warehouse transfers cannot wait on each other in opposite order. Reservation checks and stock posting must observe the same protected state.
3. Reject postings prohibited by inventory closing, frozen-period policy, invalid standard-cost effective dates, missing accounts, inappropriate warehouse company, invalid tracked identities or insufficient stock under the applicable tolerance and reservation rules.
4. Find the immediately preceding effective ledger state for the product and warehouse. Order eligible movements by business posting timestamp and then creation timestamp. Preserve creation timestamp when reproducing historical order; a replacement must not substitute document number sorting. Exact ties beyond both timestamps are an unresolved ordering case and require an explicit compatibility decision.
5. Resolve transaction incoming or outgoing cost. Standard cost governs monetary value first; otherwise use tracked serial or batch value when applicable, followed by the ordinary moving-average or ordered-layer procedure. A count reconciliation's absolute target uses its separate adjustment semantics.
6. Compute next quantity, value, valuation state and stock-value difference at the documented precisions. Zero quantity forces zero value. Preserve the calculated difference even when transaction selling price is unrelated to that cost.
7. Persist the movement with its source row and tracking references, update the current warehouse balance and tracked custody, and complete the document-specific progress effects. A saved draft has none of these submitted stock effects.
8. For perpetual inventory, construct financial postings from the actual stock-value differences, selected inventory accounts and transaction counterpart accounts. Retain company, posting date, source document, source row, cost centre, project and configured dimensions. Enforce total company-currency debits equal credits and reconcile inventory account movement with stock-value movement.
9. Register and process any downstream revaluation dependencies. Expose queued, running, completed or failed recalculation state. A failure after submission must remain visible and recoverable; the operation cannot report that all later inventory values are final while the required recalculation is unfinished.

Inventory accounts can be resolved by warehouse or, when enabled for the company, by product defaults with product-group or brand fallbacks. A missing required inventory account blocks posting. A profit-or-loss counterpart requires its cost centre. A stock transfer, reconciliation or delivery can legitimately use a balance-sheet counterpart under its own accounting contract; a universal expense-account restriction would reject supported transactions.

The following simple examples assume no tax, discount, extra charges, exchange difference or standard-cost variance. They state the net financial effect after balanced intermediary pairs are combined.

| Operation | Physical effect | Debit | Credit |
|---|---|---|---|
| Purchase receipt, ten units at five | Receive ten, stock value increases fifty | Inventory fifty | Goods received but not billed fifty |
| Supplier invoice for that already received stock | No second receipt | Goods received but not billed fifty | Supplier payable fifty |
| Delivery of six of those units | Issue six, stock value decreases thirty | Cost of goods sold thirty | Inventory thirty |
| Customer invoice for the delivery at eight each | No second dispatch | Customer receivable forty-eight | Sales revenue forty-eight |
| Customer return restoring two at original cost five | Receive two, stock value increases ten | Inventory ten | Cost of goods sold ten |
| Credit for those two sold at eight | No extra warehouse movement when the return already posted it | Referenced sales income or configured returns account sixteen | Customer receivable sixteen |
| Internal transfer of four units at five | Source minus four and twenty; target plus four and twenty | Target inventory twenty | Source inventory twenty |
| Physical shortage of one unit at five | Stock decreases one and five | Inventory adjustment expense five | Inventory five |

When the source and target use the same inventory account, an internal transfer can have zero net movement in that account while retaining both warehouse ledger legs. Goods owned at a subcontractor remain part of the company's inventory until actual consumption. A commercial delivery to another legal company invokes that company's corresponding purchase and receivable/payable contracts; do not substitute an internal warehouse transfer merely because the companies are related.

## Valuation-rate fallback contract

The ordinary valuation lookup first determines company from the warehouse when company is not supplied. For a selected batch using batch-specific valuation, it divides the sum of effective batch stock-value differences by the sum of effective batch stock quantities, excluding the current document when supplied; a zero denominator gives no usable result. A batch allocation document instead invokes its posting-time-aware batch valuation. These specialised branches precede the generic balance lookup.

The generic lookup selects the latest noncancelled ledger valuation rate greater than or equal to zero for the product and warehouse, excluding the same document type and document identifier. Its ordering is posting timestamp descending and creation timestamp descending. A retrieved zero rate is a result and is returned directly. This lookup is a fallback for missing or negative-stock cost, and is not itself bounded to the proposed posting timestamp; ordinary historical movement valuation must use the preceding-state procedure, not assume this helper supplies a historical rate.

If no qualifying ledger exists and fallbacks are enabled, select the first nonzero value from product valuation rate, product standard selling rate, then an eligible buying price in the requested currency. This final price lookup does not establish a complete preference order among several matching price records; callers needing deterministic commercial price selection must use the pricing contract. If no rate exists, zero valuation is disallowed, failure-on-missing-rate is enabled and perpetual inventory is enabled, reject the posting with a missing valuation rate explanation. Relaxing any of those gates changes the result and must be tested independently.

## Reposting after a backdated change

Reposting recalculates affected history; it does not insert a fresh receipt for each recalculated row. Start at the earliest affected movement and reuse the immediately preceding unaffected state. Visit later effective movements in posting-and-creation order. Track visited movement identifiers to avoid processing one movement twice when several dependency paths reach it. When an outgoing movement supplies a receiving transfer leg, a repack output or a manufactured product, include that dependent product and warehouse from the linked transaction row and merge its subsequent movements into the ordered work set. Update the rate and amounts on affected transaction rows, and rebuild affected financial postings where perpetual inventory requires it. A progress checkpoint must retain pending movements, visited movements, earliest affected timestamp per product and warehouse, and affected financial documents.

Consider an empty warehouse. A first receipt adds ten units at four; a delivery later issues six, initially costing twenty-four and leaving four worth sixteen. Enter another receipt of ten units at six with a posting time between those two events. Under moving average, the balance immediately before delivery becomes twenty units worth one hundred, rate five. Reposting changes delivery cost to thirty and leaves fourteen units worth seventy. The additional six of cost of goods sold is a real financial correction; changing only current quantity would leave both inventory and profit wrong.

If the delivered six were first transferred to another warehouse and then sold there, the dependent receiving leg must change from twenty-four to thirty, followed by that warehouse's outgoing cost. The adjustment must not stop at the original product-and-warehouse pair. An absolute count reconciliation can reset later quantity to its explicitly counted target; the treatment of batch and dimension reconciliations uses their separate identity-aware contracts rather than applying a blanket quantity shift through every count.

## Landed cost after stock has been sold

Receive ten units at ten each, deliver six, then allocate twenty of eligible landed cost to that receipt. The adjusted received value is one hundred twenty and per-unit cost twelve. If no other movements affect the balance, final inventory is four units worth forty-eight, cost of goods sold is seventy-two, and the landed-cost increment splits eight to inventory and twelve to cost of goods sold. Reposting and financial correction must account for the full twenty, not capitalise twenty into the four remaining units. The carrier or supplier obligation that incurred the twenty remains separately recognised; capitalisation moves the expense or clearing allocation without creating a second obligation.

For automatic landed cost, preserve item row order because rounding residual belongs to the final row. For manual allocation, zero total allocated charges is rejected by the total-basis validation even if a tolerance-only comparison would otherwise pass. The two-smallest-units tolerance is a reconciliation rule, not permission to omit an entire charge row.

## Cancellation, retry and reconciliation controls

Cancellation preserves history and reverses the transaction's effective consequences. The reviewed stock operation marks the document's effective movement rows cancelled, records inverse signed cancellation movements using the original applicable rates, and recalculates downstream effective state while excluding cancelled movements. Preserve cancellation markers on both the original and cancellation history; do not treat the inverse history as an additional effective sale or purchase. Financial cancellation creates reversing entries. Neither deleting historical rows nor adding a business return is the same operation: a return occurs at its own posting date and retains the original sale or purchase.

An in-progress valuation recalculation against the document blocks cancellation. A queued recalculation can be marked skipped and cancelled before document cancellation continues. This distinction prevents a concurrent recalculation from restoring values for a cancelled business transaction. Cancellation must also satisfy document links, closed-period and identity-ownership restrictions. Repeating an already completed cancellation must not create another inverse stock movement or financial reversal.

For every completed operation reconcile: effective warehouse quantity to ledger quantity; effective warehouse value to ledger value; cost-layer quantity and value to the aggregate where that method applies; serial and batch custody to the linked movement allocations; reservation remainder to the current active claims; and inventory financial-account movement to the sum of corresponding stock-value differences. Reconciliation errors require diagnosis against the responsible document and row, not an unexplained direct edit to a current balance.

## Acceptance and verification boundaries

Acceptance must compare quantities, inventory values, stock-value differences, ledger debit and credit effects, reservation remainder and serial or batch ownership after every operation. Include normal receipt, partial issue, full issue, zero-value receipt, explicit-rate purchase return, negative-stock transition, backdated receipt, landed cost after delivery, standard revaluation, cancellation, and repeating the same attempted posting after a failure. Document operations must either leave all required effects or leave none.

The reviewed arithmetic establishes the worked examples and branch conditions above. Complete runtime proof still requires the full transaction suites with company precision settings, inventory dimensions, inter-company transfers, serial-specific valuation and concurrent posting. A claim that every inventory behavior has been dynamically validated would exceed the evidence recorded here.
