# From a supplier receipt to cash and a customer return

A supplier delivers raw material in two lots at different prices. The company converts part of those lots into a saleable product, ships four units, invoices the customer and takes back one unit after a partial payment. This example tests whether separate purchasing, warehouse, sales and payment implementations can share one set of balances.

The invoice can be rendered in different recipient languages. Document identity, accounting status, total and open amount remain identical across translations.

## Effective configuration

One company, one supplier, one customer and one bank account use NAD. The company uses perpetual inventory, FIFO, two stock accounts mapped through separate warehouses and a single cost centre. The company converts 15 raw units into five identical finished units using a Repack stock entry. The receiving and delivery documents move quantities. The subsequent purchase invoice, sales invoice and credit note have stock updating disabled. Input tax is wholly recoverable. The example uses an exclusive 15% charge on the net amount, no additional costs, zero opening stock and no currency translation. The rate is a fixture parameter. After setting the mapped credit quantity to one returned unit, recalculate the draft taxes and totals before saving or submitting it. This gives the allocation check the intended credit of 69.00 against 96.00 still outstanding. The credit note then reduces the original sales invoice's balance. Configure two-decimal monetary precision and choose values with no fractional-cent rounding in this profile.

## Expected postings

Amounts in this table are company-currency account totals by voucher. Physical rows can be split by item, cost centre or underlying source row. A clearing or stock adjustment account used on both sides of the repack must net to zero. A party allocation retains the original invoice identity even when summarized for this table.

| ID and submitted operation | Debit | Credit | Physical or settlement consequence |
|---|---|---|---|
| OPEN · Opening journal | Bank 1,000.00 | Capital 1,000.00 | Establish opening cash. |
| GR1 · Receive 12 raw units at 10.00 | Raw inventory 120.00 | Received, unbilled 120.00 | Raw FIFO layer 12 × 10.00. |
| GR2 · Receive 8 raw units at 14.00 | Raw inventory 112.00 | Received, unbilled 112.00 | Second raw layer 8 × 14.00. |
| BILL · Invoice the two receipt rows | Received, unbilled 232.00 and input tax 34.80 | Supplier payable 266.80 | Both receipts are billed. Supplier open balance is 266.80. |
| PACK · Consume 15 and produce 5 | Packed inventory 162.00 | Raw inventory 162.00 | Consume 12 × 10.00 plus 3 × 14.00. Each finished unit receives 32.40. |
| SHIP · Deliver 4 finished units | Cost of sales 129.60 | Packed inventory 129.60 | One packed unit remains. |
| SALE · Invoice the shipment at 60.00 per unit | Customer receivable 276.00 | Sales 240.00 and output tax 36.00 | The commercial price and the earlier carrying cost have different bases. |
| PAY1 · Collect against SALE | Bank 180.00 | Customer receivable 180.00 | Customer open balance is 96.00. |
| RET · Return 1 against the delivery row | Packed inventory 32.40 | Cost of sales 32.40 | Restore the unit at the original delivery's cost. |
| CREDIT · Credit the returned unit | Sales 60.00 and output tax 9.00 | Customer receivable 69.00 | Apply to SALE. Customer open balance is 27.00. |
| PAY2 · Collect the remaining balance | Bank 27.00 | Customer receivable 27.00 | SALE closes. |
| REMIT · Pay the supplier | Supplier payable 266.80 | Bank 266.80 | BILL closes. |

After REMIT the raw bin contains five units worth 70.00 and the finished bin two units worth 64.80. Net sales of 180.00 less cost of sales of 97.20 produce gross profit of **82.80**. Ending bank is **940.20**. Assets of 1,109.80 comprise cash, both inventories and recoverable input tax of 34.80. Output tax payable of 27.00, opening equity of 1,000.00 and current profit of 82.80 reconcile to that same total. No tax settlement journal occurs in this fixture.

## Follow the transaction through the data model

Each row in the [entity index](../../schema/index.tsv) names the dictionary containing its logical fields. The same item can appear several times on one document. Retain both the originating document and its line identity when tracing costs and remaining quantities.

| Voucher | Logical record and fields | How to reconcile |
|---|---|---|
| GR1, GR2 and BILL | In [supplier receipt rows](../../schema/entities/inventory-02.json), `inventory.purchase_receipt_item` carries `quantity`, `unit_conversion_factor`, `stock_quantity` and `project_identifier`. In [supplier invoice rows](../../schema/entities/accounting-03.json), `accounting.purchase_invoice_item` carries `purchase_receipt_identifier` and `purchase_receipt_line`. | Follow each of the two invoice lines back to its own receipt line. When the invoice header’s `update_stock` is false the bill clears the prior receipt liability and creates the supplier claim without receiving another 20 units. |
| PACK and SHIP | In [warehouse movements](../../schema/entities/inventory-02.json), `inventory.stock_entry_detail` distinguishes `source_warehouse_identifier` and `target_warehouse_identifier`. Each `inventory.stock_ledger_entry` retains `originating_document_identifier`, `originating_document_line_identifier`, `warehouse_identifier`, `actual_quantity` and `stock_value_difference`. | Group movement by warehouse and item before aggregating to stock accounts. The raw issue and finished receipt can have opposite signed changes on the same voucher. |
| SALE, RET and CREDIT | The [sales invoice row](../../schema/entities/accounting-04.json) `accounting.sales_invoice_item` stores `delivery_note_identifier` and `delivery_note_line`. The [physical delivery](../../schema/entities/inventory-01.json) and [sales invoice](../../schema/entities/accounting-03.json) each have their own `is_return` and `return_against_identifier`. | RET restores physical value at the delivery cost. CREDIT affects the original financial claim. The separate links explain why the return increases stock by 32.40 but reduces receivables by 69.00. |
| PAY1, PAY2 and REMIT | In [settlement records](../../schema/entities/accounting-02.json), `accounting.payment_entry.references_rows` owns `accounting.payment_entry_reference` rows. Each records `reference_entity_type_identifier`, `reference_name_identifier`, `allocated_amount` and optional `payment_term_identifier`. | Sum only allocations for the intended party and referenced invoice, respecting cancellations. Reconcile the resulting open item separately to the control-account turnover. |

## Service contract and identities

| Operation boundary | Required source and actor scope | Committed evidence to capture |
|---|---|---|
| Receive and bill | Purchasing actor authorized for the company and warehouse. BILL carries both receipt and receipt-row references. | Accepted quantity, unit, valuation rate, supplier, document currency, item rows, receipt clearing, tax and payable. |
| Repack | Stock actor may issue from the raw warehouse and receive into the finished warehouse. Both items use the fixture's stock units. | Two item rows sharing a voucher, consumed layers, resulting stock value and both inventory account changes. |
| Deliver and invoice | Sales/stock actors share company and customer. The sales invoice item references the delivery row. | Delivery stock-ledger value and quantity, cost posting, net revenue, output tax, receivable and open-item identity. |
| Return goods and credit | Return delivery references SHIP and its row. Credit carries the original SALE and its row and applies the credit against SALE. | Increased on-hand quantity, original outgoing rate, released cost, tax reduction and decreased customer outstanding. |
| Settle | Treasury actor may post to the company bank and party accounts. Each allocation identifies a submitted invoice. | Bank leg, party control leg, party identity, allocation reference, amount and remaining open item. |

The trace identifiers identify business facts across transports. When comparing a replacement, map generated document IDs and row identities before comparing effects. Normalize journal lines by voucher, account and currency, dropping zero-net account entries **only** in the summarized view. Separately retain original item references, parties, cost centres and both stock movements. Otherwise a replacement that charged the wrong customer or silently touched stock during invoicing could pass a totals-only comparison.

## Rejection and recovery checks

1. After RET, request a second return of four units against the original four-unit shipment. Only three remain returnable. Assert a rejected submit and unchanged physical and accounting balances. Verify the same limit with two rows on a single request.
2. After CREDIT, attempt to allocate 28.00 to SALE, whose open amount is 27.00. Distinguish an excessive allocation **to this invoice** from receiving 28.00 and explicitly leaving 1.00 unallocated. Re-read the available balance when posting.
3. For a transaction-recovery test, interrupt the repack between the raw issue and finished receipt, then restart. Query both bins and both inventory accounts along with the submitted voucher. Require either the entire accepted conversion or the prior state. Separately deliver the same external request twice using the adapter's declared duplicate policy. Preserve both responses and verify one economic effect.

## Period-end report reconciliation

Use one unrestricted company, both warehouses and the same posting day for all six views. Age open items by due date and use net opening and closing columns in the trial balance. The [complete event inputs and balances](examples/receipt-to-cash.json) identify every voucher and its expected effect.

| Report | Reconciliation |
|---|---|
| Trial Balance | Eleven leaf accounts expose opening debit and credit, period debit and credit, and net closing debit and credit. Bank opened at 1,000.00, received 207.00 and paid 266.80. Receivables had equal period turnover of 276.00 per side, payables 266.80 and receipt clearing 232.00. |
| Balance Sheet | Assets were 1,109.80. Liabilities were 27.00, booked equity 1,000.00 and provisional current-period profit 82.80. Total credit was 1,109.80. |
| Profit and Loss Statement | Income was 180.00, expense 97.20 and profit 82.80. This fixture's only expense was cost of goods sold. |
| Accounts Receivable | The settled customer's open-item result was empty. Earlier non-zero allocations are recorded in the step-by-step settlement history. |
| Accounts Payable | The settled supplier's open-item result was empty. The bill had shown 266.80 outstanding before remittance. |
| Stock Balance | Raw receipts of 20 units valued at 232.00 less 15 issued at 162.00 left 5 valued at 70.00. Finished inflows of 6 valued at 194.40 include the one-unit physical return. Four shipped units valued at 129.60 left 2 valued at 64.80. |
