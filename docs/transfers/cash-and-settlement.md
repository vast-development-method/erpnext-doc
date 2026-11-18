# Cash and settlement conversions

[Structured field mappings](cash-and-settlement.json) · [All conversions](README.md)

## Add a payment entry to a bank payment order

`accounting.payment_entry` → `accounting.payment_order`

Append one bank instruction reference for this posted payment. Use its paid amount, supplier, receiving account, party bank account and payment mode. When adding to an existing order keep that order's company. The instruction does not create another payment entry.

On payment entry, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `accounting.payment_entry.record_identifier` | `accounting.payment_order_reference.reference_name_identifier` |
| `accounting.payment_entry.party_bank_account_identifier` | `accounting.payment_order_reference.bank_account_identifier` |
| `accounting.payment_entry.paid_amount` | `accounting.payment_order_reference.amount` |
| `accounting.payment_entry.paid_to_identifier` | `accounting.payment_order_reference.account_identifier` |
| `accounting.payment_entry.party_identifier` | `accounting.payment_order_reference.supplier_identifier` |
| `accounting.payment_entry.mode_of_payment_identifier` | `accounting.payment_order_reference.mode_of_payment_identifier` |

## Add a payment request to a bank payment order

`accounting.payment_request` → `accounting.payment_order`

Append the request's underlying business reference, remaining outstanding amount, supplier, payment account, bank account and payment mode. Set the instruction type to payment request. On an existing order retain its company. A full historical request amount can exceed the outstanding balance.

| Source record and field | Destination record and field |
|---|---|
| `accounting.payment_request.reference_entity_type_identifier` | `accounting.payment_order_reference.reference_entity_type_identifier` |
| `accounting.payment_request.reference_name_identifier` | `accounting.payment_order_reference.reference_name_identifier` |
| `accounting.payment_request.outstanding_amount` | `accounting.payment_order_reference.amount` |
| `accounting.payment_request.party_identifier` | `accounting.payment_order_reference.supplier_identifier` |
| `accounting.payment_request.record_identifier` | `accounting.payment_order_reference.payment_request_identifier` |
| `accounting.payment_request.mode_of_payment_identifier` | `accounting.payment_order_reference.mode_of_payment_identifier` |
| `accounting.payment_request.bank_account_identifier` | `accounting.payment_order_reference.bank_account_identifier` |
| `accounting.payment_request.account` | `accounting.payment_order_reference.account_identifier` |

## Create an overdue collection notice

`accounting.sales_invoice` → `accounting.dunning`

Select payment-schedule rows with outstanding above zero and a due date strictly before the current date. A selected row filter can narrow that set. Attach the payment-schedule row and invoice identifiers. A due-today instalment remains outside this notice.

| Source record and field | Destination record and field |
|---|---|
| `accounting.sales_invoice.customer_address_identifier` | `accounting.dunning.customer_address_identifier` |
| `accounting.payment_schedule.record_identifier` | `accounting.overdue_payment.payment_schedule` |
| `accounting.payment_schedule.owning_record_identifier` | `accounting.overdue_payment.sales_invoice_identifier` |

## Prepare a receipt or payment for a customer

`sales.customer` → `accounting.payment_entry`

Set the party kind to customer and retain its identifier. An amount, accounts, exchange rates and allocations must be established on the payment before it can settle an invoice.

| Source record and field | Destination record and field |
|---|---|
| `sales.customer.record_identifier` | `accounting.payment_entry.party_identifier` |
