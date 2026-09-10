# Accounts payable

## Local record and calculation contracts

[Supplier](../../schemas/data/record-types/supplier.json); [Supplier invoice](../../schemas/data/record-types/purchase_invoice.json); [Supplier invoice line](../../schemas/data/record-types/purchase_invoice_item.json); [Receipt](../../schemas/data/record-types/purchase_receipt.json); [Receipt line](../../schemas/data/record-types/purchase_receipt_item.json); [Payment](../../schemas/data/record-types/payment_entry.json); [Payment allocation](../../schemas/data/record-types/payment_entry_reference.json); [Payment schedule](../../schemas/data/record-types/payment_schedule.json); [Withholding entry](../../schemas/data/record-types/tax_withholding_entry.json). These local definitions provide the persistent fields, relationships, defaults and permissions. The rules below explain their business meaning and lifecycle consequences.

[Financial calculations](../../schemas/mathematics/financial-calculations.json) define evaluation order and numerical boundaries. [Accounting acceptance cases](../../schemas/mathematics/accounting-acceptance-cases.json) provide complete journal events, expected closing balances, settlement outcomes and rejection conditions. These are independently checked arithmetic expectations; they do not claim execution of an entire application.

## Business model

Accounts payable records supplier liabilities arising from purchases, reconciles them with receipts and advances, and controls payment. A purchase request authorizes a need, a purchase order commits a commercial purchase, a receipt establishes received quantities and valuation, and a supplier invoice establishes the payable claim. The supplier invoice can itself update stock, in which case it performs receipt-related stock consequences as well. Its financial interpretation depends on stock policy, item kind, linked receipt, valuation category, service deferral, intercompany treatment and invoice return status.

Persistent records include supplier and supplier group, supplier-account defaults, supplier invoice and invoice lines, receipt associations, supplier bill number and date, currency and rate, tax lines, payment schedule, advance allocations, payment holds, withholding entries, general ledger entries and party settlement entries. Each supplier invoice line preserves product identity, commercial unit and quantity, stock quantity and conversion factor, net amounts in both commercial and company currency, expense or clearing account, warehouse, project, dimensions, deferred-service dates where applicable, and source order and receipt line references.

The supplier payable line credits the rounded amount when rounding fields make it effective, otherwise grand total. It retains supplier kind and identity, payable account, due date, source invoice and settled-against invoice. For a return tied to an original bill, the settled-against reference is the original unless the return keeps its own outstanding.

## Liability composition by purchase type

| Purchase condition | Principal debit | Principal credit | Required linkage |
|---|---|---|---|
| Ordinary service, immediate expense | Expense | Supplier payable | Invoice and service line |
| Deferred service | Prepaid or deferred expense | Supplier payable | Invoice line and service interval |
| Stock invoiced after receipt | Goods received but not billed clearing account | Supplier payable | Exact receipt and receipt line |
| Stock received by invoice | Inventory account at resulting stock value, with required variance | Supplier payable | Invoice stock movement and warehouse |
| Capital asset | Asset-related account selected by asset acquisition rules | Supplier payable | Asset acquisition or asset construction relationship |
| Return or debit adjustment | Reversal of the appropriate earlier liability and cost effects | Corresponding return-side account movement | Original invoice when applicable |

The table describes decisions; individual account names are configurable. In particular, the expense-account field on a stock bill may resolve to a clearing account. It must not be interpreted as necessarily a profit-and-loss expense.

A stock invoice without stock update must clear the receipt's liability at the full billed value. If the receipt already posted standard-cost inventory and purchase price variance, the invoice must not post that purchase price variance again. This explicit current branch prevents both duplicated variance and an uncleared receipt liability. An invoice with stock update compares calculated incoming valuation with the resulting stock-ledger value and directs the difference to the appropriate variance account. For standard-cost products, the purchase price variance account is selected; otherwise expense-account fallbacks apply.

Derived receipt-to-invoice example under standard costing: receive ten units invoiced at 12.00 each, with standard inventory value 10.00 each. A receipt records inventory debit 100.00, purchase price variance debit 20.00 and received-but-unbilled credit 120.00. A later supplier invoice with stock update disabled debits received-but-unbilled 120.00 and credits supplier payable 120.00. Final inventory is 100.00, variance expense 20.00, clearing zero and supplier liability 120.00. The example specifies the no-duplicate-variance boundary; receipt valuation must also conform to the inventory specification.

## Quantity and stock-value arithmetic

For direct invoice receipt, calculated warehouse value is valuation rate rounded to its storage precision, multiplied by commercial quantity and unit conversion factor, then rounded to the line company-net precision. The inspected valuation-rate storage precision is six places when configured valuation precision is at most six, otherwise nine. Where the stock ledger has a different nonzero value, the stock-ledger value becomes the warehouse amount and the difference is posted. Stock quantity and stock value therefore cannot be derived from package count without the unit conversion factor.

A return that changes stock and is either internal or unlinked uses its actual stock-ledger movement when determining the warehouse amount. The comparison basis includes net amount, allocated item tax and landed cost; a sales incoming rate can replace the net basis. This return-specific branch is not equivalent to blindly negating the latest supplier price. Retain historical source references and original valuation context so the return follows its correct valuation path.

When the invoice bills a receipt at the same net unit rate but the currency conversion has changed, and incoming-rate adjustment from invoice price is disabled, the clearing discrepancy is commercial quantity multiplied by net rate multiplied by receipt conversion less invoice conversion. The clearing account receives that signed debit and exchange gain or loss receives the opposite signed credit. Derived example: 10 units at 5 foreign currency, receipt rate 18 and bill rate 19, produce discrepancy negative 50.00. This normalizes to clearing credit 50.00 and exchange-loss debit 50.00, clearing the receipt's original 900.00 against the invoice's 950.00 principal liability.

## Taxes, landed costs, and withholding

Purchase charges have two independent properties: addition versus deduction, and total-only versus valuation-only versus both valuation and total. Total-only tax affects supplier liability and its selected tax or expense account without increasing stock value. Valuation-only tax changes cost valuation but does not add to the supplier invoice grand total. A charge marked for both contributes to the amount due and to eligible inventory or asset value. Capitalization is restricted to the eligible part of the charge; the share allocated to a nonstock item is excluded from capitalized valuation.

Posting a charge in both categories must avoid retaining the same cost simultaneously as expense and inventory. The composition records the ordinary tax movement and the credit that removes its capitalized portion from the charge account. When the earlier receipt used temporary received-but-unbilled treatment for valuation charges, billing reverses the relevant temporary movement with preserved cost center and project. Rounding residuals in proportional charge cleanup go to the final participating row.

Supplier withholding is not simply a percentage column on a bill. It has category, effective rate period, company account, party tax identity, single and cumulative thresholds, optional excess-only taxation, linked taxable event, linked withholding event, taxable amount, actual withheld amount and historical adjustment state. It can recognize a previously under-withheld amount when a threshold is crossed and offset historical over-withholding. Lower-deduction certificates further constrain the applicable amount and rate. The detailed threshold algorithm is in [Taxation and pricing](taxation-and-pricing.md).

Derived simple bill with withholding: expense 1000.00, deductible input tax 150.00 and withholding 100.00 create expense debit 1000.00, input-tax debit 150.00, withholding-liability credit 100.00 and supplier payable credit 1050.00, assuming the configured withholding deducts from the amount payable. Paying the supplier clears 1050.00; remitting the withheld 100.00 is a separate tax-liability settlement. The threshold and legal rate are configuration inputs, not a jurisdiction-independent tax recommendation.

## Payment schedules and advances

The shared payment-schedule service can inherit terms from an order only when all lines resolve to the same source order and that order has terms or a schedule. A bill assembled from several purchase orders cannot silently take the first order's schedule as authoritative. Supplier bill date can anchor term dates. Write-off and advances reduce the amount scheduled in the appropriate monetary context. Each percentage installment receives a separately rounded commercial and company amount, and the latest installment establishes bill due date.

A supplier advance is an asset or debit party balance until allocated to a bill. When separate advance accounts are enabled, the original payment retains its own identity and the allocation later transfers the relevant amount to the invoice's payable account. Cancellation of one allocation must not cancel unrelated advance allocations. A bill can be fully settled from several advances and payments, but one reference may not receive an allocation greater than its current available amount.

Reviewed test expectation: two supplier invoices each owing 250.00 can be settled by one 500.00 payment with two reference rows; both outstanding amounts become zero. A 450.00 payment against a 250.00 invoice allocates 250.00 and retains 200.00 unallocated advance while posting total debits and credits of 450.00. Attempting to allocate 350.00 to the 250.00 claim is rejected, even if the bank payment is 350.00. Excess money is a retained advance, not permission to over-allocate the bill.

Payment submission requires zero difference amount after company conversion, allocation, included taxes, bank charges, deductions and exchange difference. Accounts used for payment deductions must be in company currency. A payment that can be saved as a draft with an unexplained difference still cannot be submitted. Supplier blocked status is checked by the payment validation sequence. The separate supplier and invoice hold predicates and their release-date differences are specified in the hold decision table below.

## Early payment discounts

An early payment discount settles the full invoice reference while the bank movement is smaller. The difference can be booked to a discount account alone or split between commercial amount and tax according to configuration. This is distinct from a trade discount applied before invoice tax calculation. In the reviewed numerical expectation, invoice principal 250.00 plus tax 45.00 creates total 295.00. A ten percent eligible early payment discount reduces bank payment to 265.50 while allocated amount remains 295.00. With tax discount splitting enabled, credit deductions are 25.00 to the configured discount account and 4.50 to the tax account. With splitting disabled, the single credit deduction is 29.50. In both cases the payment difference is zero.

These records must retain discount validity date and policy, full reference allocation, reduced money moved, and each deduction. A later auditor must be able to distinguish payment shortage, negotiated write-off, early payment discount and foreign exchange difference even when the same net bank amount results.

## Commands, reports, and acceptance

The payable boundary supports preparing a bill from orders or receipts, validating and submitting it, creating a linked return, applying or releasing a permitted hold, scheduling settlement, preparing payment, reconciling an advance, and cancelling or reversing permitted transactions. Each command identifies company, supplier, source document and source lines. Outcomes include lifecycle state, claim total, outstanding amount, generated posting identities and rejected business conditions. Supplier ageing uses settlement history, due dates and company or account currency selected by the report contract.

Acceptance fixtures must include service purchase; deferred service; direct stock receipt by invoice; receipt followed by bill; partial receipt and partial bill; standard-cost variance only once; foreign receipt and bill at different rates; valuation tax shared with a nonstock item; withholding threshold crossing; linked return; advance greater than the current bill; one payment across multiple bills; settlement discount; blocked supplier; and cancellation after reconciliation. Compare clearing accounts, stock value, expense, tax, payable, bank and unallocated advance after each operation. Require explicit reconciliation of received-but-unbilled balances so unmatched receipts remain visible rather than being written off by default.

## Invoice uniqueness, holds and release boundaries

The supplier's bill number identifies an external commercial document; the internal invoice identity identifies this system's record. When supplier-number uniqueness is enabled and the bill number is nonempty, reject another draft or submitted invoice for the same supplier and bill number whose posting date falls inside the financial-year interval resolved for the new invoice. Exclude the current internal invoice and cancelled invoices. The reviewed search does not filter existing invoices by company: a matching supplier bill in another company inside that interval can block submission. A company-scoped uniqueness rule would be a deliberate compatibility change. A blank supplier bill number does not invoke this duplicate check.

Supplier holds and individual invoice holds are separate authorities. Disabling a supplier hold clears its release date; enabling one without a hold type selects the all-transactions type. For supplier holds, an invoice-only hold affects purchase orders and supplier invoices; a payment-only hold affects supplier payments; an all-transactions hold affects both. The ordinary validation keeps a relevant supplier hold active when no release date exists or today's date is on or before release date. Release occurs after that date, using the current application date rather than the transaction's backdated posting date.

| Operation | Required checks or observed decision |
|---|---|
| Place an individual invoice on hold | Write permission; not a return; lifecycle at least submitted according to the inspected guard; outstanding amount strictly positive; supplied release date strictly after today |
| Change invoice release date | Write permission; already held; same return, lifecycle, outstanding and date checks |
| Release invoice hold | Write permission; clear hold flag and release date; original claim and ledger remain |
| Generate payment from held invoice | The generation helper treats the hold as active with no release date or a release date strictly after today |
| Validate an explicit payment reference to invoice | Reject when the invoice's hold flag remains set, without a release-date exception in this validation branch |
| Discover supplier invoices under an all-transactions supplier hold | Returns no outstanding candidates while the hold flag remains set, without checking expiry in that discovery branch |

These branch differences have observable consequences. An invoice whose release date is today can pass payment generation's date test yet fail final payment validation until its hold flag is explicitly released. An expired all-transactions supplier hold can pass the ordinary date gate yet still suppress outstanding discovery. Automatically clearing expired holds before all paths would harmonize the behavior, but that is a proposed policy and must be labeled as such. The invoice-hold lifecycle guard rejects draft state, rather than expressly requiring the submitted state; a cancelled record retaining positive outstanding must not be assumed impossible from this helper alone.

A hold changes payment eligibility, not the supplier liability. Ageing continues to show a held unpaid bill with its due date and outstanding amount. A held bill is not an expense reversal, supplier dispute settlement, or forgiveness of the debt.

## Receipt clearing and service accrual reconciliation

For each receipt line, retain received quantity, net unit rate, receipt conversion rate, receipt company amount, billed portions and returns. When a bill references the receipt, compare the same receipt-line identity; product identity alone cannot select which receipt rate, cost or accrued amount to clear. Partial bills reduce the clearing liability by their qualifying portion and leave the remainder visible.

Nonstock service receipts can accrue expense through a provisional account when that policy is enabled. A linked invoice reverses the qualifying provisional posting before recognizing its own invoice expense. The reviewed reversal basis uses the smaller of invoice quantity and receipt quantity, multiplied by receipt transaction rate and receipt conversion rate. Only receipt lines that have an effective provisional posting qualify. A service bill of six units against a ten-unit receipt at 20.00 per unit therefore reverses 120.00 of receipt expense and provisional liability; it then recognizes the six units at the invoice's approved amount. This reversal must not re-create the supplier debt already recorded by the bill.

The reconciliation result should identify each nonzero received-but-unbilled or provisional balance by company, account, receipt and line, currency, warehouse where relevant, and age. A remaining balance can represent unbilled quantity, a return, valuation charge, rate difference or unmatched relationship. Each category requires its own correcting business event. Netting unrelated suppliers or receipts until a control account reaches zero loses the information required to resolve the mismatch.

## Complete payable acceptance sequence

The machine-readable case `receipt_bill_partial_payment_and_return` fixes one company, one supplier, one currency, perpetual moving-average inventory, no taxes, quantity ten and cost 12.00 per unit. Receipt posts inventory debit 120.00 and received-but-unbilled credit 120.00. Billing posts clearing debit 120.00 and supplier payable credit 120.00. Paying 50.00 posts payable debit 50.00 and bank credit 50.00. A two-unit supplier return then reverses inventory 24.00 and liability 24.00 under the explicitly combined stock-return-and-credit event. Final inventory is eight units worth 96.00, supplier amount owed is 46.00, clearing is zero, and cash outflow is 50.00. A replacement that uses separate receipt-return and supplier-credit documents must produce the same aggregate result and preserve their distinct identities.

The case `standard_cost_receipt_billed_once` separately specifies the standard-cost valuation branch. Do not apply its 20.00 purchase variance to the moving-average sequence above. Valuation policy is a mandatory input to any supposedly complete expected posting.
