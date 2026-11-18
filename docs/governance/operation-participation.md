# Participation in cross-domain operations

A record can contribute to several operations. Use the company’s policy, current lifecycle state and the actor’s authority in addition to the entity type. The tables identify the participating records so that implementing one module does not silently exclude another.

## Posting-period controls

The period control can close a business record family for a company and interval. Evaluate the selected record family and posting date when submitting. An open period does not confer posting authority.

| Participating entity | Logical dictionary |
|---|---|
| Asset | [fixed_assets.asset](../../schema/entities/fixed-assets.json) |
| Asset capitalization | [fixed_assets.asset_capitalization](../../schema/entities/fixed-assets.json) |
| Asset repair | [fixed_assets.asset_repair](../../schema/entities/fixed-assets.json) |
| Bank clearance | [accounting.bank_clearance](../../schema/entities/accounting-01.json) |
| Delivery note | [inventory.delivery_note](../../schema/entities/inventory-01.json) |
| Dunning | [accounting.dunning](../../schema/entities/accounting-01.json) |
| Invoice discounting | [accounting.invoice_discounting](../../schema/entities/accounting-01.json) |
| Journal entry | [accounting.journal_entry](../../schema/entities/accounting-01.json) |
| Landed cost voucher | [inventory.landed_cost_voucher](../../schema/entities/inventory-01.json) |
| Payment entry | [accounting.payment_entry](../../schema/entities/accounting-02.json) |
| Payroll entry | [workforce.payroll_entry](../../schema/entities/workforce-02.json) |
| Period closing voucher | [accounting.period_closing_voucher](../../schema/entities/accounting-02.json) |
| Process deferred accounting | [accounting.process_deferred_accounting](../../schema/entities/accounting-03.json) |
| Purchase invoice | [accounting.purchase_invoice](../../schema/entities/accounting-03.json) |
| Purchase receipt | [inventory.purchase_receipt](../../schema/entities/inventory-02.json) |
| Sales invoice | [accounting.sales_invoice](../../schema/entities/accounting-03.json) |
| Stock entry | [inventory.stock_entry](../../schema/entities/inventory-02.json) |
| Stock reconciliation | [inventory.stock_reconciliation](../../schema/entities/inventory-02.json) |
| Subcontracting receipt | [subcontracting.subcontracting_receipt](../../schema/entities/subcontracting.json) |

## Bank reconciliation

Candidate voucher families for matching a statement line. The company, bank account, sign, currency, unallocated amount and submission state still decide whether an individual transaction can match.

| Participating entity | Logical dictionary |
|---|---|
| Expense claim | [workforce.expense_claim](../../schema/entities/workforce-01.json) |
| Journal entry | [accounting.journal_entry](../../schema/entities/accounting-01.json) |
| Payment entry | [accounting.payment_entry](../../schema/entities/accounting-02.json) |
| Purchase invoice | [accounting.purchase_invoice](../../schema/entities/accounting-03.json) |
| Sales invoice | [accounting.sales_invoice](../../schema/entities/accounting-03.json) |

## Financial reposting

Families eligible for the financial repost operation. A permitted type can still fail its own validations. Reapply account, currency and dimension decisions before comparing corrected balances.

| Participating entity | Logical dictionary |
|---|---|
| Expense claim | [workforce.expense_claim](../../schema/entities/workforce-01.json) |
| Journal entry | [accounting.journal_entry](../../schema/entities/accounting-01.json) |
| Payment entry | [accounting.payment_entry](../../schema/entities/accounting-02.json) |
| Purchase invoice | [accounting.purchase_invoice](../../schema/entities/accounting-03.json) |
| Purchase receipt | [inventory.purchase_receipt](../../schema/entities/inventory-02.json) |
| Sales invoice | [accounting.sales_invoice](../../schema/entities/accounting-03.json) |

## Customer advances

A receipt can reference these commitment types before a customer invoice exists. Later allocation retains the advance reference, party, currency and remaining amount.

| Participating entity | Logical dictionary |
|---|---|
| Sales order | [sales.sales_order](../../schema/entities/sales.json) |

## Supplier and employee advances

A disbursement can refer to these commitments or entitlements. Track unapplied amounts until an eligible invoice or employee claim consumes the balance.

| Participating entity | Logical dictionary |
|---|---|
| Employee advance | [workforce.employee_advance](../../schema/entities/workforce-01.json) |
| Gratuity | [workforce.gratuity](../../schema/entities/workforce-01.json) |
| Leave encashment | [workforce.leave_encashment](../../schema/entities/workforce-02.json) |
| Purchase order | [procurement.purchase_order](../../schema/entities/procurement.json) |

## Outstanding claims

These records can enter invoice-style outstanding and allocation handling. An employee reimbursement claim has a different originating event from a supplier or customer invoice.

| Participating entity | Logical dictionary |
|---|---|
| Expense claim | [workforce.expense_claim](../../schema/entities/workforce-01.json) |
| Purchase invoice | [accounting.purchase_invoice](../../schema/entities/accounting-03.json) |
| Sales invoice | [accounting.sales_invoice](../../schema/entities/accounting-03.json) |

## Independent payment cancellation

Cancellation of a linked document does not automatically cancel the payment. Resolve the allocation and retain or reverse cash only through the authorised payment operation.

| Participating entity | Logical dictionary |
|---|---|
| Payment entry | [accounting.payment_entry](../../schema/entities/accounting-02.json) |

## Recurring charges

These families participate in subscription-related handling. A subscription interval, invoice due date and settlement date describe separate events.

| Participating entity | Logical dictionary |
|---|---|
| Point of sale invoice | [accounting.point_of_sale_invoice](../../schema/entities/accounting-02.json) |
| Payment request | [accounting.payment_request](../../schema/entities/accounting-02.json) |
| Purchase invoice | [accounting.purchase_invoice](../../schema/entities/accounting-03.json) |
| Sales invoice | [accounting.sales_invoice](../../schema/entities/accounting-03.json) |

## Accounting dimensions

An enabled dimension extends transaction headers, child lines, tax rows, clearing records and posting projections. A dimension on a source line may differ from its header. Read the posting rule to select the value reaching each ledger leg.

| Participating entity | Logical dictionary |
|---|---|
| Account closing balance | [accounting.account_closing_balance](../../schema/entities/accounting-01.json) |
| Advance taxes and charges | [accounting.advance_taxes_and_charges](../../schema/entities/accounting-01.json) |
| Asset | [fixed_assets.asset](../../schema/entities/fixed-assets.json) |
| Asset capitalization | [fixed_assets.asset_capitalization](../../schema/entities/fixed-assets.json) |
| Asset depreciation schedule | [fixed_assets.asset_depreciation_schedule](../../schema/entities/fixed-assets.json) |
| Asset movement item | [fixed_assets.asset_movement_item](../../schema/entities/fixed-assets.json) |
| Asset repair | [fixed_assets.asset_repair](../../schema/entities/fixed-assets.json) |
| Asset value adjustment | [fixed_assets.asset_value_adjustment](../../schema/entities/fixed-assets.json) |
| Budget | [accounting.budget](../../schema/entities/accounting-01.json) |
| Delivery note | [inventory.delivery_note](../../schema/entities/inventory-01.json) |
| Delivery note item | [inventory.delivery_note_item](../../schema/entities/inventory-01.json) |
| Expense claim | [workforce.expense_claim](../../schema/entities/workforce-01.json) |
| Expense claim detail | [workforce.expense_claim_detail](../../schema/entities/workforce-01.json) |
| Expense taxes and charges | [workforce.expense_taxes_and_charges](../../schema/entities/workforce-01.json) |
| General ledger entry | [accounting.general_ledger_entry](../../schema/entities/accounting-01.json) |
| Journal entry account | [accounting.journal_entry_account](../../schema/entities/accounting-01.json) |
| Journal entry template account | [accounting.journal_entry_template_account](../../schema/entities/accounting-01.json) |
| Landed cost item | [inventory.landed_cost_item](../../schema/entities/inventory-01.json) |
| Landed cost taxes and charges | [inventory.landed_cost_taxes_and_charges](../../schema/entities/inventory-01.json) |
| Leave encashment | [workforce.leave_encashment](../../schema/entities/workforce-02.json) |
| Loyalty program | [accounting.loyalty_program](../../schema/entities/accounting-02.json) |
| Material request item | [inventory.material_request_item](../../schema/entities/inventory-01.json) |
| Opening invoice creation tool | [accounting.opening_invoice_creation_tool](../../schema/entities/accounting-02.json) |
| Opening invoice creation tool item | [accounting.opening_invoice_creation_tool_item](../../schema/entities/accounting-02.json) |
| Point of sale invoice | [accounting.point_of_sale_invoice](../../schema/entities/accounting-02.json) |
| Point of sale invoice item | [accounting.point_of_sale_invoice_item](../../schema/entities/accounting-02.json) |
| Point of sale profile | [accounting.point_of_sale_profile](../../schema/entities/accounting-02.json) |
| Payment entry | [accounting.payment_entry](../../schema/entities/accounting-02.json) |
| Payment entry deduction | [accounting.payment_entry_deduction](../../schema/entities/accounting-02.json) |
| Payment ledger entry | [accounting.payment_ledger_entry](../../schema/entities/accounting-02.json) |
| Payment reconciliation | [accounting.payment_reconciliation](../../schema/entities/accounting-02.json) |
| Payment reconciliation allocation | [accounting.payment_reconciliation_allocation](../../schema/entities/accounting-02.json) |
| Payment request | [accounting.payment_request](../../schema/entities/accounting-02.json) |
| Payroll entry | [workforce.payroll_entry](../../schema/entities/workforce-02.json) |
| Purchase invoice | [accounting.purchase_invoice](../../schema/entities/accounting-03.json) |
| Purchase invoice item | [accounting.purchase_invoice_item](../../schema/entities/accounting-03.json) |
| Purchase order | [procurement.purchase_order](../../schema/entities/procurement.json) |
| Purchase order item | [procurement.purchase_order_item](../../schema/entities/procurement.json) |
| Purchase receipt | [inventory.purchase_receipt](../../schema/entities/inventory-02.json) |
| Purchase receipt item | [inventory.purchase_receipt_item](../../schema/entities/inventory-02.json) |
| Purchase taxes and charges | [accounting.purchase_taxes_and_charges](../../schema/entities/accounting-03.json) |
| Request for quotation item | [procurement.request_for_quotation_item](../../schema/entities/procurement.json) |
| Sales invoice | [accounting.sales_invoice](../../schema/entities/accounting-03.json) |
| Sales invoice item | [accounting.sales_invoice_item](../../schema/entities/accounting-04.json) |
| Sales order | [sales.sales_order](../../schema/entities/sales.json) |
| Sales order item | [sales.sales_order_item](../../schema/entities/sales.json) |
| Sales taxes and charges | [accounting.sales_taxes_and_charges](../../schema/entities/accounting-04.json) |
| Shipping rule | [accounting.shipping_rule](../../schema/entities/accounting-04.json) |
| Stock entry | [inventory.stock_entry](../../schema/entities/inventory-02.json) |
| Stock entry detail | [inventory.stock_entry_detail](../../schema/entities/inventory-02.json) |
| Stock reconciliation | [inventory.stock_reconciliation](../../schema/entities/inventory-02.json) |
| Subcontracting order | [subcontracting.subcontracting_order](../../schema/entities/subcontracting.json) |
| Subcontracting order item | [subcontracting.subcontracting_order_item](../../schema/entities/subcontracting.json) |
| Subcontracting receipt | [subcontracting.subcontracting_receipt](../../schema/entities/subcontracting.json) |
| Subcontracting receipt item | [subcontracting.subcontracting_receipt_item](../../schema/entities/subcontracting.json) |
| Subscription | [accounting.subscription](../../schema/entities/accounting-04.json) |
| Subscription plan | [accounting.subscription_plan](../../schema/entities/accounting-04.json) |
| Supplier quotation | [procurement.supplier_quotation](../../schema/entities/procurement.json) |
| Supplier quotation item | [procurement.supplier_quotation_item](../../schema/entities/procurement.json) |

## Workforce financial audit trail

Trace amendment and cancellation lineage for workforce records that carry pay, benefit or reimbursement consequences.

| Participating entity | Logical dictionary |
|---|---|
| Expense claim | [workforce.expense_claim](../../schema/entities/workforce-01.json) |
| Gratuity | [workforce.gratuity](../../schema/entities/workforce-01.json) |
| Leave encashment | [workforce.leave_encashment](../../schema/entities/workforce-02.json) |
| Payroll entry | [workforce.payroll_entry](../../schema/entities/workforce-02.json) |
| Salary slip | [workforce.salary_slip](../../schema/entities/workforce-02.json) |

## Party correspondence

Use the customer or supplier as the correspondence party while retaining the specific contact, role and source transaction.

| Participating entity | Logical dictionary |
|---|---|
| Customer | [sales.customer](../../schema/entities/sales.json) |
| Supplier | [procurement.supplier](../../schema/entities/procurement.json) |
