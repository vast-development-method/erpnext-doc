# Purchasing and inventory

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Import and export licence balances

Bind the invoice line to a licence and its item allowance. Retain assessed values on the cost-insurance-freight and free-on-board bases when applicable. Validate both residual value and residual quantity before posting.

**Worked case.** The import allowance has 50 kg and 450 units of licence currency remaining. An operator submits an invoice line for 40 kg assessed at 451. Reject the amount overrun and retain balances of 50 kg and 450. Hindi and English error messages identify the same licence, allowance and exceeded value.

### Additional decisions

Maintain a movement per company, licence, direction, item and originating invoice line. Store the quantity with its unit and the assessed value with its currency. If invoice and authorisation currencies differ, persist the approved conversion basis before testing a value ceiling. Make the remaining quantity and value reproducible from approved limits and posted movements. Retain the licence and corresponding movements when an invoice is cancelled, recording a reversing movement only once. The calculated balance must survive two buyers posting for the same licence concurrently.

### Detailed workflow and cases

<a id="import-and-export-licence-balances-2"></a>

#### Operating rules

| Operation | Input and observable result |
|---|---|
| Assess utilisation | Return quantity available, value available, requested amounts and the first exceeded limit for each line. No posting. |
| Apply invoice | Reassess all lines against the same locked/versioned balance. Commit the invoice references and movements together. |
| Show utilisation | Present the separate import allowances and export commitment with drill-down to the invoice line and any reversal. |

<a id="import-and-export-licence-balances-3"></a>

#### Acceptance cases

Localise “amount remaining”, “export commitment” and the maximum-available error with separate message keys. Preserve licence numbers, file numbers and externally assigned item codes exactly. An English-language invoice and a Hindi-language licence report must select the same licence ID, currency and ratio.

- **Within both limits.** An import allowance has 80 kg and 700 units of licence currency available. Posting 30 kg assessed at 250 leaves 50 kg and 450. A replay of the same committed line retains both balances.
- **Independent limits.** From 50 kg and 450 remaining, an invoice for 40 kg assessed at 451 fails the value check. Neither balance moves. An export transaction against the same licence must leave the import movements intact.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/advance_authorisation_licence.md).

## Demand simulation before procurement

Select forecast horizon, demand basis, current balance and expected receipt dates. Include component demand for bundles when enabled. Simulate alternative receipt quantities before making a supplier commitment.

**Worked case.** A scenario has 18 units on hand, 6 arriving before demand and demand of 30, with no backorders. The planner adds a simulated receipt of 10 before demand. Projected lost units change from 6 to 0 and projected closing stock becomes 4. No order is submitted. Translating the item caption and forecast bucket labels preserves all quantities and dates.

### Additional decisions

Use a dated forecast snapshot identified by company, item, warehouse, time bucket, unit, model version and input cutoff. Retain the input history, open receipts, starting stock and any bundle-to-component conversion factors that applied when the scenario was run. A scenario records changes to dated supply or demand and references a baseline. An order proposal records supplier, lines, dates, planning assumptions and review state. A planner can save several simulations without affecting on-order stock. A buyer with purchasing authority can turn an approved version into one Purchase Order.

### Detailed workflow and cases

<a id="demand-simulation-before-procurement-2"></a>

#### Operating rules

For an explicitly defined lost-sales scenario with no backordering, allocate available units to demand once per bucket. Lost units equal the positive excess of demand over opening stock plus arriving supply. Carry unconsumed units forward. The example defines a replacement planning convention. Historical lost sales require a separate evidence source such as unserved requests, with the observation window and calculation disclosed.

<a id="demand-simulation-before-procurement-3"></a>

#### Acceptance cases

Risk codes, warehouse keys, bundle composition and numeric series are independent of the viewer’s language. Translate dashboard labels and risk descriptions, localise month/quantity displays, and keep collaborators’ notes in the language authored. Country and language preferences must never select the model or change a delivery date.

- **What-if.** Starting with 18 units, an arrival of 6 before demand of 30 yields 6 lost units. A simulated arrival of 10 more before that demand yields 4 closing units and zero lost units. Both users see identical time-series values when viewing the plan in different languages.
- **Commit.** Converting an approved proposal twice returns the same order ID. If supply changed after the reviewed snapshot, require a new preview and preserve the earlier scenario. A viewer can review the scenario without submitting an order.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/advanced_procurement.md).

## Lot acceptance sampling

Select a sampling plan for the receipt lot, record readings and determine disposition. A failed lot inspection can route the entire linked receipt quantity to rejected inventory. Keep sample size and affected lot size separate.

**Worked case.** A required receipt line has 12 received units and a submitted inspection with a rejected disposition. Apply the lot disposition to the linked receipt. The line records 0 accepted and 12 rejected units. German and English reports render the same disposition code, sample identities and quantities.

### Additional decisions

Record the source document line, item, lot, unit, inspection stage, plan/table version, level, limits, parameter and sample number for each observation. Store the table decision separately from execution status and override disposition. A supervisor’s exception carries an actor, time and reason. A stage action must distinguish releasing saleable stock, accepting a receipt into a rejected warehouse and halting shipment.

Translate inspector prompts, defect descriptions, dispositions and customer certificate captions. Keep numeric readings, AQL scales, inspection-level codes, sample numbers and identifiers invariant. A German certificate and an English inspection screen must report the same counts and disposition. Record the language of free-text observations. Localised status captions must never be compared by the decision engine. Public materials and static source do not establish certification or runtime equivalence.

### Detailed workflow and cases

<a id="lot-acceptance-sampling-2"></a>

#### Operating rules

| Fixture | Expected observation |
|---|---|
| All required readings accepted for a completed inspection | Eligible for release under the configured gate. Report the captured plan and count zero rejected rows in each class. |
| Major limit 1, one rejected major reading, all other readings accepted, no override | Under the rule that a rejected major reading rejects the inspection, reject the lot. A threshold-only plan can accept this lot at a limit of one. Record the sampling policy as part of the plan so the inspection can be reproduced. |
| Receipt for 12 units linked to a submitted rejected inspection | Under the recovered receipt disposition the line has 0 accepted and 12 rejected. A draft inspection cannot satisfy the submission check. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/aql_quality_assurance.md).

## Milk collection and component pricing

Find the submitted price basis matching milk type, collection warehouse and effective date. Component price equals fat rate times fat fraction plus solids-not-fat rate times its fraction. Multiply by volume before applicable incentives or deductions.

**Worked case.** Simplified pricing uses fat/SNF rates of 80 and 30, readings of 4.0% and 8.5%, volume 100 and no deductions or incentives. Calculate the price and replay the same uniquely identified device reading. Unit price is 5.75 and total value 575. Volume and payable are recorded once. A decimal comma or decimal point used for display leaves the stored readings and resulting price unchanged.

### Additional decisions

A collection agent records producer, centre, collection timestamp, product, measurement unit, device observation IDs, volume and quality. Preserve raw and corrected readings and the rate version. A dispatch groups producer collections into a vehicle run. The receiver records physically accepted quantity, any discrepancy and quality result. Supplier settlement references accepted measurements and the rate contract. A corrected reading or rate version generates an auditable adjustment after settlement.

Translate producer receipts, quality terms, discrepancy reasons and units for display. Retain numeric measurements, instrument codes and the original label in the device record. Afrikaans decimal-comma and English decimal-point renderings of the SNF reading must lead to the same rate calculation. Never infer a conversion between litres and kilograms from language.

### Detailed workflow and cases

<a id="milk-collection-and-component-pricing-2"></a>

#### Operating rules

- In simplified pricing with deductions and incentives disabled, fat rate 80 and SNF rate 30 with readings 4.0% and 8.5% give `(80 × 4 + 30 × 8.5) / 100 = 5.75`. For 100 volume units the value is 575 in the rate’s currency. A replayed device reading cannot double the volume or value.
- A vehicle picks up 100 and delivers 98 in the same unit. The dock comparison reports a variance of −2. The operator must give an explicit disposition before a discrepancy changes the supplier’s payable.
- With no applicable rate, show the missing centre, date and milk type, and leave the supplier settlement unposted.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/dairy.md).

## Channel receipt synchronization

Map the external product and location to the internal item and warehouse. Business sales and consumer channel orders have distinct origins. Link each completed receipt event to one inventory receipt.

**Worked case.** A mapped warehouse receives an external completion event for three units. The same event arrives twice and the operator changes language between deliveries. Return the same ERP receipt reference twice and post one receipt for three units. SKU, event ID, warehouse and quantity stay identical across languages.

### Additional decisions

The warehouse operator maintains scoped item and location mappings. A connector identity receives an event with a channel, seller account, external event and order references, event kind, line identifiers and quantities. Record both systems' identifiers before acknowledging the event. Match cancellations and receipts to their originating records. Keep an unrecognised item or target location in an actionable queue with the original payload, a reason code and the last successful step. Reprocessing must resume without adding a second stock movement.

Keep the channel's original SKU, Unicode delivery address, buyer name and document references. Provide translated product descriptions and error messages separately. Resolve the operator's reconciliation screen using the operator's language and customer correspondence using the order's recipient language. Where a description is missing, display the source description with its language. Matching must use seller-scoped IDs even when two translations of a product name are identical.

### Detailed workflow and cases

<a id="channel-receipt-synchronization-3"></a>

#### Operating rules

| Acceptance example | Expected result |
|---|---|
| A completed receipt for three units arrives twice. The second delivery occurs after the operator switches from English to Afrikaans. | One Purchase Receipt for three units, the same local reference on both acknowledgements, and a translated status on the operator's screen. |
| A consumer order identifies SKU `C-24`, which has no mapping, but its display name matches a different local item. | No item or ledger entry is inferred from the name. After a mapping is approved, replay posts exactly the original quantity for `C-24`. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/erpnext_easyecom.md).

## Warehouse scanning and transfers

A scanner identifies item, lot, bin and unit at receipt, count, pick, pack and dispatch. Convert handling units into stock units before committing the movement. Reuse the operation identity when scanning again after a lost response.

**Worked case.** Bin A holds 20 stock units, bin B is empty and each carton contains six units. An Afrikaans-speaking picker transfers two cartons to B and a German-speaking supervisor reopens the confirmed transfer. Show 8 units in A and 12 in B, with one posted transfer even if the scanner retries. Translating the unit label, item description or bin caption preserves the conversion factor, barcode and quantities.

### Detailed workflow and cases

<a id="warehouse-scanning-and-transfers-1"></a>

#### Operating rules

| Floor action | Identity and quantity inputs | Business consequence |
|---|---|---|
| Inquire or count | Company, warehouse, bin, item, lot/serial where required, observed quantity and unit | Inquiry is read-only. Save a count against a dated stock snapshot. A supervisor reviews discrepancies before submitting a stock adjustment. |
| Request, receive or transfer | Request or purchase line reference, source and destination, lot, unit and accepted quantity | A request is demand. Only posting the appropriate inventory document changes the ledger. Record rejected quantities separately from accepted stock. |
| Inspect, pick and pack | Quality result, order line, source bin, optional lot, quantity and package | Make the inspection visible to authorized staff. Prevent release of held stock. Link picks and packages to the order without duplicating an outbound movement. |
| Dispatch or print | Delivery reference, packed quantities and permission to post or reprint | Post one stock issue for a confirmed delivery. Label printing or reprinting returns the same item, bin or package identity without moving inventory. |

<a id="warehouse-scanning-and-transfers-2"></a>

#### Acceptance cases

1. Start with 20 units in bin A and zero in B. An Afrikaans-speaking picker moves two six-unit cartons from A to B. A German-speaking supervisor sees 8 and 12 units. Repeating the same confirmed scan changes neither figure. The result retains the original scan, carton unit ID and conversion factor 6.
2. An Arabic-speaking operator prints a bilingual package label. The description and handling instructions use the configured translations and print direction. The machine-readable barcode, lot number and SKU retain their canonical character sequence and scan to the same package after reprint.
3. An English count reports 10 units. A transfer posts before an Afrikaans reviewer approves it. Surface the changed stock snapshot, obtain a recount or authorized reconciliation, and retain the original observation. Language changes cannot turn a rejected variance into a posted adjustment.
4. A lot fails inspection. The picker sees the hold reason in their selected language while the raw inspection comment remains intact. Packing the same lot through another locale or retrying after a connection loss cannot release it.

Exact offline or delayed synchronization, scanner compatibility, reservation timing, valuation, serial/batch enforcement and supported language packs need evidence from a matched server/client installation.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/wms.md).
