# Payment requests, payment orders and bank guarantees

A payment request asks a party to pay or records the intention to pay a party. A payment order groups eligible obligations for disbursement. A submitted payment voucher changes the ledger and settlement records. A bank guarantee records the issuing institution's commitment and its commercial reference. Each has its own identity and approval state.

## Relational contract

| Record | Relationships and durable values |
|---|---|
| Payment request | One company, direction, document kind and originating document identity, party kind and identity, transaction currency, party account currency, requested total, open amount, channel, optional bank account and recipient contact. Carry the request identity on payment allocations. |
| Requested installment | Ordered child of one request. Retain the amount and the installment identity when known. An identified installment can occur only once per request. A request can instead contain rows without installment identifiers. |
| Payment order | One company, order kind, selected bank and funding account. A supplied bank account must exist, be enabled, belong to the company and be designated as a company account. The bank account supplies the bank and ledger account. |
| Payment order allocation | Ordered child of one order. Retain supplier, method, amount, originating document kind and identity, associated payment request where applicable, and the identity of any generated journal. Two allocations can concern different requests on the same commercial invoice. |
| Bank guarantee | Direction, amount, beneficiary, bank, guarantee number, customer or supplier, optional underlying order, project, validity interval, margin money, charges and deposit or account references. |

## Determine the requestable amount

Require the referenced document kind and identity and the same company. Supported references are customer and supplier orders, customer and supplier invoices, point-of-sale invoices and fee assessments. A supplied party kind must exist on the reference. A supplied party identity must agree with that field. A selected company bank account must belong to this company. A selected party bank account must belong to this party and party kind. A disabled account fails in either case.

| Reference | Calculation before deducting other requests |
|---|---|
| Order | Rounded total when effective, otherwise grand total, less advances paid. If party account and transaction currency differ, divide advances by the order conversion rate before subtraction. |
| Customer or supplier invoice | Use invoice outstanding when party account and transaction currencies match. Otherwise divide outstanding by the invoice conversion rate. For a customer invoice with point-of-sale charging and matching telephone-payment rows, use the sum of the matching tender amounts. |
| Point-of-sale invoice | Take the first telephone tender matching the selected payment account. No eligible row contributes zero. |
| Fee assessment | Use its outstanding amount. |

A positive basis is rounded to currency precision. A nonpositive basis yields zero. For an ordinary reference, sum the outstanding amounts of other submitted requests for the same document kind and identity, converting them back to transaction currency when necessary. Reject a zero request and a combined amount greater than the reference basis. Shopping-cart orders have a separate requestability branch. Compare the request and its selected installment amounts at the request's total precision.

Installment rounding can produce a small discrepancy. For a reference with a payment schedule, compute the surplus of independently rounded schedule rows over the schedule’s target total. Cap that surplus at the number of installments multiplied by half of one minor unit and round at the configured precision. When selected rows exceed the requestable amount by a positive excess within that cap, subtract the excess from the last selected row and from the request total. A larger difference requires correcting the input. With three scheduled amounts of 33.34 each, target 100.01 and precision two, the excess is 0.01 and the last requested amount can fall to 33.33.

## Request and order state transitions

Submission initializes request outstanding in party account currency. An outward request enters **Initiated** and an inward request enters **Requested**. For an inward request choose the configured payment channel. A telephone request passes the amount and currency to the provider. A payment-link request can send a communication to its recipient. Authorization or completion on an unpaid ordinary payment link prepares and submits the payment, with optional invoice creation. On the telephone path the authorization handler marks the request paid and clears request outstanding. Reconcile the associated tender or voucher separately. A paid request status alone cannot identify the company journal that moved cash.

For each payment order allocation, re-read the referenced document on submission and reserve its identity during the check. It must be submitted, belong to the same company when it specifies one, and be unpaid. A reference already in another submitted order of the same kind is ineligible. Submitting changes applicable requests to **Payment Ordered**. Preparing a journal groups unpaid rows by supplier and optional payment method. Reserve and re-read the selected allocation rows before creating a draft, so repeated preparation cannot pick rows already tied to a journal. Debit the supplier account once per reference and credit the funding account for the sum. A cash payment method chooses a cash journal. The draft records its originating order, and each chosen allocation records its draft journal. Only a subsequent authorized posting changes money balances.

Given two requests for 75 and 25 on the same invoice and a posted supplier debit of 80 against that invoice, allocate in payment-order row sequence. Allocate 75 to the first request and 5 to the second. Twenty remains on the second. Cancellation reverses the allocations, restores the ordered state and clears only the links for the affected journal. Cancelling the payment order itself derives each request state from the remaining amount. A fully restored positive total goes back to **Initiated** or **Requested** by direction, a nonpositive remainder becomes **Paid**, and an intermediate positive remainder becomes **Partially Paid**. Reading allocation rows requires authority on the owning payment order.

## Guarantee admission and use

A received guarantee can draw its amount, customer and project from a sales order. A provided guarantee can draw its amount and supplier from a purchase order. The lookup requires access to the guarantee function and returns those limited fields. Validate that at least one customer or supplier is present. Submission additionally requires a guarantee number, named beneficiary and issuing bank. Issuance records an undertaking. A bank charge, blocked deposit, realized claim or payment requires the appropriate posting and its own account and currency facts.

For example, a 10,000 guarantee with a 2,000 margin deposit and a 75 commission has three distinct measures. Guarantee exposure is 10,000. If the bank actually takes 2,075, a separate accounting event may debit the deposit asset 2,000 and fee expense 75 and credit the bank 2,075. A later release of the deposit clears the deposit account. The guarantee face value does not enter that cash movement.
