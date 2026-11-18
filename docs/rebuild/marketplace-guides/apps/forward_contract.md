# Forward Contract

[Business workflow and acceptance cases](../../../capabilities/guides/accounting.md#forward-exchange-contract-allocation).

Finbyz Tech Pvt Ltd lists this treasury extension for major versions 14 and 15. It records a bank FX hedge, applies the forward rate during a payment and records gain or loss when unused capacity is cancelled. This localized workflow uses the currencies and quotation direction on each contract. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/forward_contract) · [Publisher operating guide](https://finbyz.tech/erpnext/apps/forward-contract-erpnext)

## Documented business flow

1. Treasury records the bank reference, import or export designation, contract currency and amount, spot rate, premium or discount, any bank spread, booking date and booked rate. A start and end date define the maturity period. Save and submit the contract. The guide relates the forward quote to spot plus a premium or minus a discount. It does not establish how every bank spread is incorporated. [Booking guide](https://finbyz.tech/erpnext/apps/forward-contract-erpnext)
2. Accounts selects the customer or supplier and paid-from and paid-to accounts on a Payment Entry. Its utilization table can allocate a partial amount from one contract or draw on several contracts for a single payment. Submission reduces the outstanding contract capacity. [Payment allocation](https://cloud.frappe.io/marketplace/apps/forward_contract)
3. To close unused capacity, treasury supplies the cancellation date, amount, rate and bank account. Adding a cancellation records its details, reduces the outstanding amount and generates a Journal Entry for the exchange gain or loss. [Cancellation guide](https://finbyz.tech/erpnext/apps/forward-contract-erpnext)

## FinByz-attributed historical controller

A public combined package preserves a Forward Contract controller credited to FinByz. It calculates booking rate as current rate plus premium less margin. Export cancellation uses booked rate less cancellation rate, while import uses the reverse difference. The signed difference times cancelled units determines gain or loss. Positive amounts credit the exchange gain/loss account and debit the bank; a zero difference adds a cancellation row without creating a journal. The remaining amount is booked amount less total utilization and total cancellations. A negative result raises an error; zero gives Closed. This copy uses INR- and USD-specific fields for bank-limit calculations. In the target, the bank facility selects the exposure and reporting currencies and each amount carries its own currency. The combined package's revision does not identify the marketplace build. [Rate and bank-limit calculation](https://github.com/kaushik-bansode/rodtep_claim_and_forward_contract/blob/5856a74219aff730aea17f79e9b81a372b5895fa/rodtep_claim_and_forward_contract/rodtep_claim_and_forward_contract/doctype/forward_contract/forward_contract.py#L41) · [Cancellation and journal legs](https://github.com/kaushik-bansode/rodtep_claim_and_forward_contract/blob/5856a74219aff730aea17f79e9b81a372b5895fa/rodtep_claim_and_forward_contract/rodtep_claim_and_forward_contract/doctype/forward_contract/forward_contract.py#L83)

## Proposed rebuild contract

The example's quote convention, settlement assumptions and reversal treatment specify target behavior. The publisher materials do not establish the app's exact journal-sign implementation, rounding sequence, maturity-date enforcement or reversal mechanics.

[Read the consolidated workflow](../../../capabilities/guides/accounting.md#forward-exchange-contract-allocation-3).
