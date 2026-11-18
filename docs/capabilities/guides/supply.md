# Purchasing and inventory

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Import and export licence balances

Bind the invoice line to a licence and its item allowance. Retain assessed values on the cost-insurance-freight and free-on-board bases when applicable. Validate both residual value and residual quantity before posting.

**Worked case.** The import allowance has 50 kg and 450 units of licence currency remaining. An operator submits an invoice line for 40 kg assessed at 451. Reject the amount overrun and retain balances of 50 kg and 450. Hindi and English error messages identify the same licence, allowance and exceeded value.

### Additional decisions

Maintain a movement per company, licence, direction, item and originating invoice line. Store the quantity with its unit and the assessed value with its currency. If invoice and authorisation currencies differ, persist the approved conversion basis before testing a value ceiling. Make the remaining quantity and value reproducible from approved limits and posted movements. Retain the licence and corresponding movements when an invoice is cancelled, recording a reversing movement only once. The calculated balance must survive two buyers posting for the same licence concurrently.

## Demand simulation before procurement

Select forecast horizon, demand basis, current balance and expected receipt dates. Include component demand for bundles when enabled. Simulate alternative receipt quantities before making a supplier commitment.

**Worked case.** A scenario has 18 units on hand, 6 arriving before demand and demand of 30, with no backorders. The planner adds a simulated receipt of 10 before demand. Projected lost units change from 6 to 0 and projected closing stock becomes 4. No order is submitted. Translating the item caption and forecast bucket labels preserves all quantities and dates.

### Additional decisions

Use a dated forecast snapshot identified by company, item, warehouse, time bucket, unit, model version and input cutoff. Retain the input history, open receipts, starting stock and any bundle-to-component conversion factors that applied when the scenario was run. A scenario records changes to dated supply or demand and references a baseline. An order proposal records supplier, lines, dates, planning assumptions and review state. A planner can save several simulations without affecting on-order stock. A buyer with purchasing authority can turn an approved version into one Purchase Order.

## Lot acceptance sampling

Select a sampling plan for the receipt lot, record readings and determine disposition. A failed lot inspection can route the entire linked receipt quantity to rejected inventory. Keep sample size and affected lot size separate.

**Worked case.** A required receipt line has 12 received units and a submitted inspection with a rejected disposition. Apply the lot disposition to the linked receipt. The line records 0 accepted and 12 rejected units. German and English reports render the same disposition code, sample identities and quantities.

### Additional decisions

Record the source document line, item, lot, unit, inspection stage, plan/table version, level, limits, parameter and sample number for each observation. Store the table decision separately from execution status and override disposition. A supervisor’s exception carries an actor, time and reason. A stage action must distinguish releasing saleable stock, accepting a receipt into a rejected warehouse and halting shipment.

Translate inspector prompts, defect descriptions, dispositions and customer certificate captions. Keep numeric readings, AQL scales, inspection-level codes, sample numbers and identifiers invariant. A German certificate and an English inspection screen must report the same counts and disposition. Record the language of free-text observations. Localised status captions must never be compared by the decision engine. Public materials and static source do not establish certification or runtime equivalence.

## Milk collection and component pricing

Find the submitted price basis matching milk type, collection warehouse and effective date. Component price equals fat rate times fat fraction plus solids-not-fat rate times its fraction. Multiply by volume before applicable incentives or deductions.

**Worked case.** Simplified pricing uses fat/SNF rates of 80 and 30, readings of 4.0% and 8.5%, volume 100 and no deductions or incentives. Calculate the price and replay the same uniquely identified device reading. Unit price is 5.75 and total value 575. Volume and payable are recorded once. A decimal comma or decimal point used for display leaves the stored readings and resulting price unchanged.

### Additional decisions

A collection agent records producer, centre, collection timestamp, product, measurement unit, device observation IDs, volume and quality. Preserve raw and corrected readings and the rate version. A dispatch groups producer collections into a vehicle run. The receiver records physically accepted quantity, any discrepancy and quality result. Supplier settlement references accepted measurements and the rate contract. A corrected reading or rate version generates an auditable adjustment after settlement.

Translate producer receipts, quality terms, discrepancy reasons and units for display. Retain numeric measurements, instrument codes and the original label in the device record. Afrikaans decimal-comma and English decimal-point renderings of the SNF reading must lead to the same rate calculation. Never infer a conversion between litres and kilograms from language.

## Channel receipt synchronization

Map the external product and location to the internal item and warehouse. Business sales and consumer channel orders have distinct origins. Link each completed receipt event to one inventory receipt.

**Worked case.** A mapped warehouse receives an external completion event for three units. The same event arrives twice and the operator changes language between deliveries. Return the same ERP receipt reference twice and post one receipt for three units. SKU, event ID, warehouse and quantity stay identical across languages.

### Additional decisions

The warehouse operator maintains scoped item and location mappings. A connector identity receives an event with a channel, seller account, external event and order references, event kind, line identifiers and quantities. Record both systems' identifiers before acknowledging the event. Match cancellations and receipts to their originating records. Keep an unrecognised item or target location in an actionable queue with the original payload, a reason code and the last successful step. Reprocessing must resume without adding a second stock movement.

Keep the channel's original SKU, Unicode delivery address, buyer name and document references. Provide translated product descriptions and error messages separately. Resolve the operator's reconciliation screen using the operator's language and customer correspondence using the order's recipient language. Where a description is missing, display the source description with its language. Matching must use seller-scoped IDs even when two translations of a product name are identical.

## Warehouse scanning and transfers

A scanner identifies item, lot, bin and unit at receipt, count, pick, pack and dispatch. Convert handling units into stock units before committing the movement. Reuse the operation identity when scanning again after a lost response.

**Worked case.** Bin A holds 20 stock units, bin B is empty and each carton contains six units. An Afrikaans-speaking picker transfers two cartons to B and a German-speaking supervisor reopens the confirmed transfer. Show 8 units in A and 12 in B, with one posted transfer even if the scanner retries. Translating the unit label, item description or bin caption preserves the conversion factor, barcode and quantities.
