# From a supplier receipt to cash and a customer return

A supplier delivers raw material in two lots at different prices. The company converts part of those lots into a saleable product, ships four units, invoices the customer and takes back one unit after a partial payment. This example tests whether separate purchasing, warehouse, sales and payment implementations can share one set of balances.

The submitted sales invoice from this trading scenario was also rendered in English, Afrikaans, German, Chinese and Arabic. Compare its stable record ID, customer, status, total and outstanding amount with the five translated headings in the [language observations](../marketplace-guides/languages/observed.json).

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

1. After RET, request a second return of four units against the original four-unit shipment. Only three remain returnable. Assert a rejected submit and unchanged physical and accounting balances. Verify the same limit with two rows on a single request. [Upstream return guards](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/sales_and_purchase_return.py#L285-L367)
2. After CREDIT, attempt to allocate 28.00 to SALE, whose open amount is 27.00. Distinguish an excessive allocation **to this invoice** from receiving 28.00 and explicitly leaving 1.00 unallocated. Re-read the available balance when posting. [Allocation checks](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_entry/payment_entry.py#L479-L592)
3. For a replacement's transaction-recovery test, interrupt the repack between the raw issue and finished receipt, then restart. Query both bins and both inventory accounts along with the submitted voucher. Require either the entire accepted conversion or the prior state. Separately deliver the same external request twice using the adapter's declared duplicate policy. Preserve both responses and verify one economic effect. These two probes are rebuild acceptance requirements. An authenticated transport and operation-specific replay evidence are necessary to qualify a particular site.

## Verification

The [machine-readable fixture](cost-flow.json) supplies commands, earlier voucher IDs, expected stock deltas, net account postings and 15 closing controls. The [JSON Schema](cost-flow.schema.json) defines operation-specific input shapes and decimal strings. Run the independent decision model from the repository root with the following command.

```sh
python3 docs/rebuild/integrated/verify.py
```

The verifier recalculates consumption from FIFO layers, billing from receipt values, the original delivery rate, the commercial price, the tax basis and open-item allocations. It compares both inventory controls and both party controls after **each** of 12 postings. The optional [source witness](reference-stock.py) executes the pinned valuation classes, their real numeric converter, and 22 deterministic upstream unit tests without starting a site. Give it checkouts containing the two commits in the source links.

```sh
python3 docs/rebuild/integrated/reference-stock.py /path/to/erpnext /path/to/frappe
```

The pure valuation code agreed with all six physical movements. A separate [live reference exercise](../live/README.md) submitted the twelve vouchers to the pinned ERPNext and Frappe site. With the partial credit recalculated before submission, all journal and stock movements and the 15 closing controls matched. The original invoice went from 276.00 to 96.00 after the first receipt, to 27.00 after the credit, and to zero after the second receipt. The fixture records the expected open amount by original invoice after every event. Six [report readbacks](../live/reports/README.md) check the committed scenario through accounting, ageing and stock reports.

The live run also exposed a meaningful difference between a customer's net balance and their open invoices. If a program maps the full sales invoice to a draft credit, changes its quantity to one and retains its old full-document totals, the allocation guard reads those stale totals before the general recalculation. It can direct the credit to its own open item. On this fixture the original invoice still has 69.00 outstanding after the second receipt, while the customer control account nets to zero. Preserve the voucher-level allocation and the effective flag when reproducing this path. [Allocation guard](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/accounts_controller.py#L243-L270) · [Validation order](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/accounts_controller.py#L335-L355)

## Reference decisions

| Decision | Pinned source |
|---|---|
| Receipt stock and provisional liability | [Purchase receipt account selection and posting](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/purchase_receipt/purchase_receipt.py#L540-L900) |
| Invoice liability, clearing and purchased tax | [Supplier control entry](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py#L1051-L1136), [receipt clearing](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py#L1420-L1485), [tax legs](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py#L1747-L1867) |
| Ordered layer consumption and conversion | [FIFO decisions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/valuation.py#L52-L159), [repack valuation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_entry/stock_entry.py#L2265-L2273) |
| Stock value paired to the contra account | [Stock controller's per-row accounting](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/stock_controller.py#L950-L1035) |
| Invoice, credit note and original sales return cost | [Customer and income legs](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/sales_invoice.py#L1925-L2115), [rate from referenced stock movement](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/sales_and_purchase_return.py#L937-L1015) |
| Settlement | [Party and allocation leg](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_entry/payment_entry.py#L1494-L1660), [bank leg](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_entry/payment_entry.py#L1781-L1817) |
