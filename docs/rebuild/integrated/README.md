# From a supplier receipt to cash and a customer return

A supplier delivers raw material in two lots at different prices. The company converts part of those lots into a saleable product, ships four units, invoices the customer and takes back one unit after a partial payment. This example tests whether separate purchasing, warehouse, sales and payment implementations can share one set of balances.

The submitted sales invoice from this trading scenario was also rendered in English, Afrikaans, German, Chinese and Arabic. Compare its stable record ID, customer, status, total and outstanding amount with the five translated headings in the [language observations](../marketplace-guides/languages/observed.json).

## Expected postings

The [twelve-voucher trace](../../transactions/receipt-to-cash.md#expected-postings) gives every debit, credit, FIFO movement and open-item balance under the [fixture configuration](../../transactions/receipt-to-cash.md#effective-configuration). Use the [actor and source-row contracts](../../transactions/receipt-to-cash.md#service-contract-and-identities) and [rejection and recovery checks](../../transactions/receipt-to-cash.md#rejection-and-recovery-checks) when replaying it. The interruption and duplicate-request checks are acceptance requirements for a replacement. Qualifying a deployment requires its authenticated transport and observed operation replay.

[Upstream return guards](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/sales_and_purchase_return.py#L285-L367) · [Allocation checks](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_entry/payment_entry.py#L479-L592)

## Verification

The [machine-readable fixture](cost-flow.json) supplies commands, earlier voucher IDs, expected stock deltas, net account postings and 15 closing controls. The [JSON Schema](cost-flow.schema.json) defines operation-specific input shapes and decimal strings. Run the independent decision model from the repository root with the following command.

```sh
python3 docs/rebuild/integrated/verify.py
```

The verifier recalculates consumption from FIFO layers, billing from receipt values, the original delivery rate, the commercial price, the tax basis and open-item allocations. It compares both inventory controls and both party controls after **each** of 12 postings. The optional [source witness](reference-stock.py) executes the pinned valuation classes, their real numeric converter, and 22 deterministic upstream unit tests without starting a site. Give it checkouts containing the two commits in the source links.

```sh
python3 docs/rebuild/integrated/reference-stock.py /path/to/erpnext /path/to/frappe
```

The pure valuation code agreed with all six physical movements. A separate [live reference exercise](../live/README.md) submitted the twelve vouchers to the isolated reference site. With the partial credit recalculated before submission, all journal and stock movements and the 15 closing controls matched. The original invoice went from 276.00 to 96.00 after the first receipt, to 27.00 after the credit, and to zero after the second receipt. The fixture records the expected open amount by original invoice after every event. Six [report readbacks](../live/reports/README.md) check the committed scenario through accounting, ageing and stock reports.

The live run also exposed a meaningful difference between a customer's net balance and their open invoices. If a program maps the full sales invoice to a draft credit, changes its quantity to one and retains its old full-document totals, the allocation guard reads those stale totals before the general recalculation. It can direct the credit to its own open item. On this fixture the original invoice still has 69.00 outstanding after the second receipt, while the customer control account nets to zero. Preserve the voucher-level allocation and the effective flag when reproducing this path. [Allocation guard](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/accounts_controller.py#L243-L270) · [Validation order](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/accounts_controller.py#L335-L355)

## Reference decisions

| Decision | Source evidence |
|---|---|
| Receipt stock and provisional liability | [Purchase receipt account selection and posting](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/purchase_receipt/purchase_receipt.py#L540-L900) |
| Invoice liability, clearing and purchased tax | [Supplier control entry](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py#L1051-L1136), [receipt clearing](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py#L1420-L1485), [tax legs](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py#L1747-L1867) |
| Ordered layer consumption and conversion | [FIFO decisions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/valuation.py#L52-L159), [repack valuation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_entry/stock_entry.py#L2265-L2273) |
| Stock value paired to the contra account | [Stock controller's per-row accounting](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/stock_controller.py#L950-L1035) |
| Invoice, credit note and original sales return cost | [Customer and income legs](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/sales_invoice.py#L1925-L2115), [rate from referenced stock movement](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/sales_and_purchase_return.py#L937-L1015) |
| Settlement | [Party and allocation leg](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_entry/payment_entry.py#L1494-L1660), [bank leg](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_entry/payment_entry.py#L1781-L1817) |
