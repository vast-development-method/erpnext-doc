# Forward Contract

Finbyz Tech Pvt Ltd lists this treasury extension for major versions 14 and 15. It records a bank FX hedge, applies the forward rate during a payment and records gain or loss when unused capacity is cancelled. This localized workflow uses the currencies and quotation direction on each contract. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/forward_contract) · [Publisher operating guide](https://finbyz.tech/erpnext/apps/forward-contract-erpnext)

## Documented business flow

1. Treasury records the bank reference, import or export designation, contract currency and amount, spot rate, premium or discount, any bank spread, booking date and booked rate. A start and end date define the maturity period. Save and submit the contract. The guide relates the forward quote to spot plus a premium or minus a discount. It does not establish how every bank spread is incorporated. [Booking guide](https://finbyz.tech/erpnext/apps/forward-contract-erpnext)
2. Accounts selects the customer or supplier and paid-from and paid-to accounts on a Payment Entry. Its utilization table can allocate a partial amount from one contract or draw on several contracts for a single payment. Submission reduces the outstanding contract capacity. [Payment allocation](https://cloud.frappe.io/marketplace/apps/forward_contract)
3. To close unused capacity, treasury supplies the cancellation date, amount, rate and bank account. Adding a cancellation records its details, reduces the outstanding amount and generates a Journal Entry for the exchange gain or loss. [Cancellation guide](https://finbyz.tech/erpnext/apps/forward-contract-erpnext)

## Proposed rebuild contract

Keep the currency pair, quote denominator, units, rate precision and approved booked rate on the contract. Treat utilizations and cancellations as individually identified movements. Remaining contract units equal booked units less effective utilizations and effective cancellations. Assign one payment allocation ID per contract leg. Apply the legs atomically and serialize competing draws on the same remaining balance. Link the cancellation to its journal and preserve both sides of a subsequently authorized reversal.

Translate hedge-type, gain/loss and status captions. Fix bank references, account IDs, currency codes and rational rate direction independently of language. Input may use locale-specific decimals; after explicit locale parsing, persist canonical decimals. Render monetary values with their currency codes. A French-speaking clerk and German-speaking reviewer can share a contract while maintaining the same signed rate and amount.

| Acceptance example | Expected result |
|---|---|
| Book an exporter sale of USD 1,000 at 17.50 NAD per USD. Allocate USD 600 to one receipt and cancel USD 100 at 17.20 NAD per USD. Ignore fees in this target example. | USD 300 remains. For the stated sell-USD direction, closing USD 100 at a 0.30 differential gives a NAD 30 gain, with equal bank debit and gain credit under the example's cash-settled convention. A translation change leaves both journal legs intact. |
| Two clerks attempt to use USD 200 each from the remaining USD 300. | Only one draw succeeds at that balance. The other receives the available USD 100 and a localized rejection. No partial posting occurs. |
| A payment uses two contracts with different rates or one leg has the wrong currency pair. | Preserve the amount and booked rate on each valid leg. A mismatched pair rejects the whole request before balances or journals change. |

The example's quote convention, settlement assumptions and reversal treatment specify target behavior. The publisher materials do not establish the app's exact journal-sign implementation, rounding sequence, maturity-date enforcement or reversal mechanics.
